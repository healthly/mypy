#!/usr/bin/env python
#coding=utf-8
"""Change passwords on the named machines. passmass host1 host2 host3 . . .
Note that login shell prompt on remote machine must end in # or $. """

import pexpect
import sys, getpass

USAGE = '''passmass host1 host2 host3 . . .'''
COMMAND_PROMPT = '[$#] '
TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'
SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'

def login(host, user, password, port):

    child = pexpect.spawn('ssh -l %s %s -p %s'%(user, host, port))
    #fout = file ("LOG.TXT","wb")
    #child.setlog (fout)

    i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, '[Pp]assword: '])
    if i == 0: # Timeout
        print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
        print child.before, child.after
        sys.exit (1)
    if i == 1: # SSH does not have the public key. Just accept it.
        child.sendline ('yes')
        child.expect ('[Pp]assword: ')
    child.sendline(password)
    # Now we are either at the command prompt or
    # the login process is asking for our terminal type.
    i = child.expect (['Permission denied', TERMINAL_PROMPT, COMMAND_PROMPT])
    if i == 0:
        print 'Permission denied on host:', host
        sys.exit (1)
    if i == 1:
        child.sendline (TERMINAL_TYPE)
        child.expect (COMMAND_PROMPT)
    return child

# (current) UNIX password:
def change_password(child, user, oldpassword, newpassword):

    child.sendline('sudo passwd ' + user) 
    #i = child.expect(['[Oo]ld [Pp]assword', '.current.*password', '[Nn]ew [Pp]assword'])
    # Root does not require old password, so it gets to bypass the next step.
    #if i == 0 or i == 1:
    #    child.sendline(oldpassword)
    child.expect('[Nn]ew [Pp]assword')
    child.sendline(newpassword)
    i = child.expect(['[Nn]ew [Pp]assword', '[Rr]etype', '[Rr]e-enter'])
    if i == 0:
        print 'Host did not like new password. Here is what it said...'
        print child.before
	child.send (chr(3)) # Ctrl-C
        child.sendline('') # This should tell remote passwd command to quit.
        return
    child.sendline(newpassword)

def main():

    if len(sys.argv) <= 1:
        print USAGE
        return 1

    #user = raw_input('Username: ')
    user = 'lvmama_admin'
    password = '123456'
    newpassword = '654321'
    #newpassword = getpass.getpass('New Password: ')
    newpasswordconfirm = '654321'
    if newpassword != newpasswordconfirm:
        print 'New Passwords do not match.'
        return 1

    for host in sys.argv[1:]:
	port = '22'
        child = login(host, user, password, port)
        if child == None:
            print 'Could not login to host:', host
            continue
        print 'Changing password on host:', host
        change_password(child, user, password, newpassword)
        child.expect(COMMAND_PROMPT)
        child.sendline('exit')

if __name__ == '__main__':
    try:
        main()
    except pexpect.ExceptionPexpect, e:
        print str(e)


