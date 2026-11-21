"""Location diagnostics survive shared adapters without executing customer code."""
import json
import os
import subprocess
import sys

import pytest
from meritz.strategy_runner import StrategySession, validate_code


@pytest.mark.parametrize('label', ['한', '😀'])
def test_compiler_error_columns_are_unicode_not_utf8(label):
    result = validate_code(f'x = "{label}"; return 1\ndef on_bar(ctx):\n return {{}}')
    assert not result['valid']
    assert result['errors'][0]['line'] == 1
    assert result['errors'][0]['column'] == 10


def test_worker_annotation_compilation_contract_is_preserved():
    invalid = 'def on_bar(ctx):\n def g(x: (yield)): pass\n return {}'
    assert not validate_code(invalid)['valid']
    valid = 'def on_bar(ctx: UnknownType):\n return {"action":"hold"}'
    assert validate_code(valid)['valid'], 'Annotations remain postponed as in the existing worker'
    if sys.platform == 'darwin':
        with StrategySession(valid) as session:
            assert session.decide({}) == {'action': 'hold'}


@pytest.mark.parametrize('pattern', ['"1+"*30000+"1"', '"("*500+"1"+")"*500', '"not "*10000+"True"'])
def test_complex_code_is_rejected_in_small_stack_thread_without_host_crash(pattern):
    probe = '''import threading,json
from meritz.strategy_runner import validate_code
threading.stack_size(512*1024)
expression = EXPRESSION
def check():
 result=validate_code("def on_bar(ctx):\\n x="+expression+"\\n return {}")
 print(json.dumps({'valid':result['valid'],'errors':result['errors']}),flush=True)
t=threading.Thread(target=check);t.start();t.join()
'''.replace('EXPRESSION', pattern)
    process = subprocess.run([sys.executable, '-c', probe], capture_output=True, text=True, timeout=15)
    assert process.returncode == 0, process.stderr
    result = json.loads(process.stdout)
    assert not result['valid'] and result['errors']


@pytest.mark.parametrize('opening', ['(', '[', '{'])
def test_unclosed_bracket_points_at_opener(opening):
    result = validate_code('def on_bar(ctx):\n value = ' + opening)
    assert not result['valid']
    assert result['errors'][0]['line'] == 2
    assert result['errors'][0]['column'] == 10


@pytest.mark.parametrize('code,line,column', [('x = 1 + \\\n', 1, 10), ('def on_bar(ctx):\n v = 1 + \\', 2, 11)])
def test_line_continuation_at_eof_points_at_backslash_line(code, line, column):
    # 3.11 tokenize 는 (다음 줄, 0), 3.12+ 는 (그 줄, 끝) 을 주므로 버전과 무관하게 compile() 위치로 고정한다.
    result = validate_code(code)
    assert not result['valid']
    assert result['errors'][0]['line'] == line
    assert result['errors'][0]['column'] == column
    assert 'EOF' in result['errors'][0]['message']


def test_regular_parameter_tables_and_lists_remain_valid():
    code = f'params = {dict((str(i), i) for i in range(32))!r}\nvalues = {list(range(100))!r}\ndef on_bar(ctx):\n return {{"action":"hold"}}'
    assert validate_code(code)['valid']
    oversized = 'def on_bar(ctx):\n value = ' + 'not ' * 1000 + 'True'
    result = validate_code(oversized)
    assert not result['valid'] and result['errors'][0]['line'] == 2
    assert result['errors'][0]['column'] > 1
    assert '문장' in result['errors'][0]['message']


def test_elif_chain_has_a_located_limit_before_parser():
    code = 'def on_bar(ctx):\n if False: pass\n' + ' elif False: pass\n' * 1000 + ' return {}'
    result = validate_code(code)
    assert not result['valid']
    assert 'elif' in result['errors'][0]['message']
    assert result['errors'][0]['line'] == 131


@pytest.mark.parametrize('separator', ['\x0c', '\x85', '\u2028', '\u2029'])
def test_non_newline_unicode_does_not_shift_compiler_location(separator):
    result = validate_code(f'# comment {separator} text\nx = "한"; return 1\ndef on_bar(ctx): return {{}}')
    assert not result['valid']
    assert result['errors'][0]['line'] == 2
    assert result['errors'][0]['column'] == 10


def test_cr_only_lines_match_python_line_numbering():
    result = validate_code('def on_bar(ctx):\r x = "😀"; )')
    assert not result['valid']
    assert result['errors'][0]['line'] == 2 and result['errors'][0]['column'] == 11


def test_nested_elif_chains_rejected_before_parser(monkeypatch):
    from meritz import strategy_runner
    lines = ['def on_bar(ctx):']
    for depth in range(4):
        indent = ' ' * (depth + 1)
        lines += [indent + 'if False: pass'] + [indent + 'elif False: pass'] * 100
        lines += [indent + 'else:']
    lines += ['     return {}']
    def forbidden_parse(*args, **kwargs):
        pytest.fail('Oversized conditional chains must not reach ast.parse')
    monkeypatch.setattr(strategy_runner.ast, 'parse', forbidden_parse)
    result = validate_code('\n'.join(lines))
    assert not result['valid']
    assert '256' in result['errors'][0]['message']
    assert result['errors'][0]['line'] > 200
    assert result['limits']['totalConditionals'] == 256


def test_unclosed_string_inside_brackets_points_at_string():
    code = 'def on_bar(ctx):\n value = (\n  """unfinished'
    result = validate_code(code)
    assert not result['valid']
    assert result['errors'][0]['line'] == 3
    assert result['errors'][0]['column'] == 3
    assert 'multi-line string' in result['errors'][0]['message']


@pytest.mark.parametrize('expression', ['ctx' + '.value' * 250, 'ctx' + '()' * 250, 'ctx' + '[0]' * 160])
def test_postfix_chains_near_statement_budget_in_small_stack(expression):
    probe = """import threading,json
from meritz.strategy_runner import validate_code
threading.stack_size(512*1024)
def check():
 result=validate_code(SOURCE)
 print(json.dumps({'valid':result['valid'],'errors':result['errors']}),flush=True)
t=threading.Thread(target=check);t.start();t.join()
""".replace('SOURCE', repr('def on_bar(ctx):\n value = ' + expression + '\n return {}'))
    process = subprocess.run([sys.executable, '-c', probe], capture_output=True, text=True, timeout=15)
    assert process.returncode == 0, process.stderr
    assert json.loads(process.stdout)['valid']
