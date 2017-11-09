import sys, subprocess, re
import pexpect

##
## read log into memory, requires removal of dead paths
##
store = []
highest = -1
for i, line in enumerate(sys.stdin):
    print(line.lstrip().rstrip())
    if line.lstrip().rstrip() == 'false' or line.lstrip().rstrip().startswith('0: '):
        print("skip")
        continue
    length = len(line) - len(line.lstrip())
    improved = line
    if ':' in line:
        improved = line.split(':',1)[1].lstrip().rstrip().split('(',1)[1].rsplit(')',1)[0]
        improved = improved.replace(', ', '###').replace(',', ', ').replace('###', ', ')
    if length <= highest:
        for j, (l, prev) in reversed(list(enumerate(store))):
            if l >= length:
                store.pop(j)
            else:
                break
    store.append((length, improved))
    highest = length
print(store[0])
print(len(store))

###
### now simulate path onto lift.lps
###
child = pexpect.spawnu('lpssim lift.lps')

child.expect('\?')
text = child.before

options = list(filter(None,text.split('initial state: ')[1].split('\n')))[1:]
# print(store[0][1])
tried_skipping = False
for (length, line) in store:
    should_be = line.lstrip().rstrip()
    if should_be == 'False':
        break

    print("next:",should_be)
    # print(initial_state)
    done = False
    for option in options:
        # if options.startswith('initial state'):
        #     continue
        brr = option.split('[', 1)[1].rsplit(']',1)[0]

        if brr in should_be:
            done = True
            next_option = option.split(":",1)[0]
            child.sendline(str(next_option))
            child.expect('\?')
            text = child.before
            options = list(filter(None,text.split('current state: ')[1].split('\n')))[1:]
            tried_skipping = False
            break
    if not done:
        print("ERROR: did not find next statement")
        for option in options:
            print(option)
        print("try skipping")
        if not tried_skipping:
            tried_skipping = True
            continue
        else:
            sys.exit(1)


###
### save the trace
###
child.sendline('s trace.trc')
child.expect('trace saved')
child.kill(1)
print("trace saved")
# child.interact()
# child.kill(1)
