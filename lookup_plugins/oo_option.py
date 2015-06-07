#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: expandtab:tabstop=4:shiftwidth=4

'''
oo_option lookup plugin for openshift-ansible

Usage:

    - debug:
      msg: "{{ lookup('oo_option', '<key> default=<default_value>') }}"

This returns, by order of priority:

* if it exists, the `opt_<key>` ansible variable. This variable is set by `bin/cluster --option <key>=<value> …`
* if it exists, the envirnoment variable named `<key>`
* if present, the `<default_value>` passed in the lookup statement
* if none of the above conditions are met, empty string is returned
'''

from ansible import utils, errors
import os

# Reason: disable too-few-public-methods because the `run` method is the only
#     one required by the Ansible API
# Status: permanently disabled
# pylint: disable=too-few-public-methods
class LookupModule(object):
    ''' oo_option lookup plugin main class '''

    # Reason: disable unused-argument because Ansible is calling us with many
    #     parameters we are not interested in.
    #     The lookup plugins of Ansible have this kwargs “catch-all” parameter
    #     which is not used
    # Status: permanently disabled unless Ansible API evolves
    # pylint: disable=unused-argument
    def __init__(self, basedir=None, **kwargs):
        ''' Constructor '''
        self.basedir = basedir

    # Reason: disable unused-argument because Ansible is calling us with many
    #     parameters we are not interested in.
    #     The lookup plugins of Ansible have this kwargs “catch-all” parameter
    #     which is not used
    # Status: permanently disabled unless Ansible API evolves
    # pylint: disable=unused-argument
    def run(self, terms, inject=None, **kwargs):
        ''' Main execution path '''

        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        ret = []

        for term in terms:
            params = term.split()
            option_name = params[0]

            paramvals = {
                'default': ''
            }

            try:
                for param in params[1:]:
                    name, value = param.split('=')
                    assert name in paramvals
                    paramvals[name] = value
            except (ValueError, AssertionError), ex:
                raise errors.AnsibleError(ex)

            opt_key = 'opt_' + option_name
            if opt_key in inject:
                ret.append(inject[opt_key])
            elif option_name in os.environ:
                ret.append(os.environ[option_name])
            else:
                ret.append(paramvals['default'])

        return ret
