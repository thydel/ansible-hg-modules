#!/usr/bin/python

DOCUMENTATION = '''
#include documentation.yml
'''

EXAMPLES = '''
#include examples.yml
'''

def main():
    
    argument_spec = dict(
        cwd = dict(required=True, aliases=['src', 'repos', 'repository'], type='str'),
        com = dict(required=True, aliases=['comment', 'commentary'], type='str'),
        user = dict(required=False, type='str'),
        addremove = dict(required=False, choices=BOOLEANS, type='bool', default=True),
        )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    info = {}
    ansible_facts = { 'hg_commit': info }
    changed = False

    def getargs(arg):
        globals()[arg] = module.params.get(arg)
        
    # map(getargs, argument_spec.keys())
    for arg in argument_spec.keys():
        getargs(arg)

    cmd_hg = ['hg', '--cwd', cwd]
    cmd_id = cmd_hg + ['id']
    cmd_st = cmd_hg + ['st']

    cmd_comm = cmd_hg + ['com']
    if user: cmd_comm += ['-u', user]
    if addremove: cmd_comm += ['-A']
    cmd_comm += ['-m', com]

    rc, out, err = module.run_command(cmd_id, check_rc=True)
    info['id'] = out.split()[0];

    rc, out, err = module.run_command(cmd_st, check_rc=True)
    status = out
    info['status'] = status.rstrip('\n').split('\n')

    if not status:
        module.exit_json(changed=changed, ansible_facts=ansible_facts)

    changed = True
    if module.check_mode: 
        module.exit_json(changed=changed, ansible_facts=ansible_facts)
    rc, out, err = module.run_command(cmd_comm, check_rc=True) # todo error ?
    rc, out, err = module.run_command(cmd_id, check_rc=True)
    info['id'] = out.split()[0]

    module.exit_json(changed=changed, ansible_facts=ansible_facts)

# this is magic, see lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>

main()
