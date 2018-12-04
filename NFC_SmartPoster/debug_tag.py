# read tag in a loop, and write to it
import nfc
from nfc.clf import RemoteTarget
import time
import signal

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

def make_smartposter(resource, titles, action = 'default'):
    record = nfc.ndef.SmartPosterRecord(resource)
    for title in titles:
        lang, text = title.split(':', 1) if ':' in title else ('en', title)
        record.title[lang] = text
    if not action in ('default', 'exec', 'save', 'edit'):
        print("error: action not one of 'default', 'exec', 'save', 'edit'")
        return
    record.action = action

    return nfc.ndef.Message(record)

def program_remote_tag(message, tag):
    if not tag.ndef.is_writeable:
        print("This Tag is not writeable.")
        return False
    tag.ndef.message = message
    print("Programmed tag OK.")
    return True

def program(uri):
    print("Connecting to tag...")
    after5s = lambda: time.time() - started > 5;print(".")
    after2s = lambda: time.time() - started > 2;print(".")
    started = time.time()
    tag = clf.connect(rdwr={'on-connect': lambda tag: False}, terminate=after2s) # close connection when tag is found
    if (tag):
        smartposter = make_smartposter(uri, ["en-US:Other search engines exist"])
        program_remote_tag(smartposter, tag)
    else:
        print("tag not detected!")

def mute():
    print("mute %s %s %s" % (clf.device.vendor_name, clf.device.chipset_name, clf.device.product_name))
    clf.device.mute()

def read_tag(timeout =5):
    print("Connecting to tag...")
    after5s = lambda: time.time() - started > timeout;print(".")
    started = time.time()
    result = clf.connect(llcp={}, rdwr={'on-connect': lambda tag: False}, terminate=after5s) # close connection when tag is found
    if (result):
        print( result.type) # 'Type4Tag'
        if (result.ndef):
            print("records %d"% len(result.ndef.records)) # 1
            if (result.ndef.records):
                print(result.ndef.records[0].__dict__)
        else:
            print("tag has NO records!")
        print(result)
    else:
        print("Tag not detected!")
    return result
    
def read_loop():
    while True:
        if read_tag(timeout=2):
            mute()
            time.sleep(2)

# init reader
clf = nfc.ContactlessFrontend()
if not clf.open("usb"):
    raise Exception("Cannot load drivers for USB reader!")
print("NFC reader ready")
uri1 = "https:\\www.google.com"
uri2 = "https:\\www.mbed.com"
sig = signal.signal(signal.SIGINT, keyboardInterruptHandler)

while True:
    print("Press 1 for read tag, 2 to write google.com, 3 to write url mbed.com , 4 to mute\r\n 5 to loop")
    response = str(input("?"))
    if response == "1":
        read_tag()
    if response == "2":
        program(uri1)    
    if response == "3":
        program(uri2)
    if response == "4":
        mute()
    if response == "5":
        read_loop()