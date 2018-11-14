I created a small project to help recreate this issue https://github.com/ansible/ansible/issues/48691

## Problem

From jinja2 using the template module, we are currently accessible other device variables
using hostvars[<otherdevice>].var1 in multiple places. This is working very well for us as long as all the variables are stored in group_vars and host_vars.

Since our data are fairly dynamic we wanted to move away from group_vars and host_vars so we investigated the cache plugins. we tried both redis and jsonfile and for both we observed that it would take much longer for the jinja2 template to render if we are using either cache plugin (redis been much slower)

After some investigation it, it seams to me that ansible fetch the latest hostvars for a given device from the cache EACH time a variable is accessed.
For example in the short snippet below ansible will it the cache 2 times. one for the if and one to render the variable.

```jinja
{% if hostvars["deviceA"].site == "xxx" %}
    {{ hostvars["deviceA"].site  }}
{% endif %}
```
This happen even if the variable is not part of the facts but is coming from the dynamic inventory.

### performance results with ansible 2.7.1

There are 2 environments, one using the jsonfile cache plugin and the other one using the same data saved in hostvars.
when rendering the same jinja2 template with the same variables, it's easy to see the difference of execution time.

- host_vars: 26.3s
- jsonfile: 43.6s
- redis: 548s

### Steps to reproduce
```
cd 1_no_cache
ansible-playbook pb.gen.facts.yaml
ansible-playbook pb.render_tpl.yaml
```
```
cd 2_with_cache
ansible-playbook pb.gen.facts.yaml
ansible-playbook pb.render_tpl.yaml
```
> profile_tasks is enabled by default
