"""Reasonably complete set of BDD steps for testing a REST API.

Some state is set-up and shared between steps using the context variable. It is
reset at the start of every scenario by
:func:`restapiblueprint.features.environment.before_scenario`

"""
from nose.tools import assert_equal
import behave
import decorator
import jinja2
import jpath
import json
import os
import purl
import requests
import time


def _decode_parameter(value):
    """Get BDD step parameter, redirecting to env var if start with $."""
    if value.startswith('$'):
        return os.environ.get(value[1:], '')
    else:
        return value


def _get_data_from_context(context):
    """Use context.text as a template and render against any stored state."""
    data = ''
    try:
        if context.text:
            data = context.text
    except AttributeError:
        data = ''
    # Always clear the text to avoid accidental re-use.
    context.text = u''
    # NB rendering the template always returns unicode.

    result = jinja2.Template(data).render(context.template_data)
    return result.encode('utf8')


@decorator.decorator
def dereference_step_parameters_and_data(f, context, *parameters):
    """Decorator to dereference step parameters and data.

    This involves two parts:

        1) Replacing step parameters with environment variable values if they
        look like an environment variable (start with a "$").

        2) Treating context.text as a Jinja2 template rendered against
        context.template_data, and putting the result in context.data.

    """
    decoded_parameters = map(_decode_parameter, parameters)
    context.data = _get_data_from_context(context)
    f(context, *decoded_parameters)


@behave.given('I am using server "{server}"')
@dereference_step_parameters_and_data
def using_server(context, server):
    context.server = purl.URL(server)


@behave.given('I set {var} header to "{value}"')
@dereference_step_parameters_and_data
def set_header(context, var, value):
    # We must keep the headers as implicit ascii to avoid encoding failure when
    # the entire HTTP body is constructed by concatenating strings.
    context.headers[var.encode('ascii')] = value.encode('ascii')


@behave.given('I use query OAuth with key="{key}" and secret="{secret}"')
@dereference_step_parameters_and_data
def query_oauth(context, key, secret):
    context.auth = requests.auth.OAuth1(
        key, secret, signature_type='query')


@behave.given('I use header OAuth with key="{key}" and secret="{secret}"')
@dereference_step_parameters_and_data
def header_oauth(context, key, secret):
    context.auth = requests.auth.OAuth1(
        key, secret, signature_type='auth_header')


@behave.given('I set context "{variable}" to {value}')
@dereference_step_parameters_and_data
def set_config(context, variable, value):
    setattr(context, variable, json.loads(value))


@behave.when(
    'I poll GET "{url_path_segment}" until JSON at path "{jsonpath}" is')
@dereference_step_parameters_and_data
def poll_GET(context, url_path_segment, jsonpath):
    json_value = json.loads(context.data)
    url = context.server.add_path_segment(url_path_segment)
    for i in range(context.n_attempts):
        response = requests.get(url, headers=context.headers, auth=context.auth)
        if jpath.get(jsonpath, response.json) == json_value:
            return
        time.sleep(context.pause_between_attempts)
    raise AssertionError(
        'Condition not met after %d attempts' % context.n_attempts)


@behave.when('I send an OPTIONS request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def options_request(context, url_path_segment):
    context.response = requests.options(
        context.server.add_path_segment(url_path_segment))


@behave.when('I send a PATCH request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def patch_request(context, url_path_segment):
    url = context.server.add_path_segment(url_path_segment)
    context.response = requests.patch(
        url, data=context.data, headers=context.headers, auth=context.auth)


@behave.when('I send a PUT request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def put_request(context, url_path_segment):
    url = context.server.add_path_segment(url_path_segment)
    context.response = requests.put(
        url, data=context.data, headers=context.headers, auth=context.auth)


@behave.when('I send a POST request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def post_request(context, url_path_segment):
    url = context.server.add_path_segment(url_path_segment)
    context.response = requests.post(
        url, data=context.data, headers=context.headers, auth=context.auth)


@behave.when('I send a GET request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def get_request(context, url_path_segment):
    headers = context.headers.copy()
    if not context.data:
        # Don't set the Content-Type if we have no data because no data is not
        # valid JSON.
        if 'Content-Type' in headers:
            del headers['Content-Type']
    url = context.server.add_path_segment(url_path_segment)
    context.response = requests.get(
        url, data=context.data, headers=headers, auth=context.auth)


@behave.when('I send a DELETE request to "{url_path_segment}"')
@dereference_step_parameters_and_data
def delete_request(context, url_path_segment):
    url = context.server.add_path_segment(url_path_segment)
    context.response = requests.delete(
        url, headers=context.headers, auth=context.auth)


@behave.when('I store the JSON at path "{jsonpath}" in "{variable}"')
@dereference_step_parameters_and_data
def store_for_template(context, jsonpath, variable):
    context.template_data[variable] = jpath.get(
        jsonpath, context.response.json)


@behave.then('the response status should be "{status}"')
@dereference_step_parameters_and_data
def response_status(context, status):
    assert_equal(context.response.status_code, int(status))


@behave.then('the {var} header should be')
@dereference_step_parameters_and_data
def check_header(context, var):
    assert_equal(context.response.headers[var], context.data.encode('ascii'))


@behave.then('the {var} header should be "{value}"')
@dereference_step_parameters_and_data
def check_header_inline(context, var, value):
    assert_equal(context.response.headers[var], value.encode('ascii'))


@behave.then('the JSON should be')
@dereference_step_parameters_and_data
def json_should_be(context):
    json_value = json.loads(context.data)
    assert_equal(context.response.json, json_value)


@behave.then('the JSON at path "{jsonpath}" should be {value}')
@dereference_step_parameters_and_data
def json_at_path_inline(context, jsonpath, value):
    json_value = json.loads(value)
    assert_equal(jpath.get(jsonpath, context.response.json()), json_value)


@behave.then('the JSON at path "{jsonpath}" should be')
@dereference_step_parameters_and_data
def json_at_path(context, jsonpath):
    json_value = json.loads(context.data)
    assert_equal(jpath.get(jsonpath, context.response.json), json_value)
