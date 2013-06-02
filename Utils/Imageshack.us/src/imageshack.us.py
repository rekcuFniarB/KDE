#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os, sys, re
import subprocess as run
import simplejson as json
import requests as www

config = {
    'url':'http://post.imageshack.us/upload_api.php',
    'key': '',
    'UA': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/21.0',
    'referer': 'http://imageshack.us/?no_multi=1'
    }
config_file = os.path.join(os.environ.get('HOME'), '.config','imageshack.json')

File = sys.argv[1].decode('utf-8') # Picture file
Filename = os.path.basename(File)

if not os.path.exists(config_file):
    # Getting api key from the imageshack.us main page
    key_expr = re.compile(r'<input type="hidden" name="key" value="(.+?)"')
    try:
        r = www.get('http://imageshack.us/', headers={'User-Agent': config['UA'], 'Referer': 'http://imageshack.us/'})
        if r.ok:
            page =  r.content
            config['key'] = key_expr.search(page).group(1)
    except:
        sys.stderr.write("Failed to get the api key.\n")
        #raise
        sys.exit(1)
    # Generating config file and storing api key
    with open (config_file, 'wb') as f:
        json.dump(config, f)
else:
    # Loading config (api key etc.)
    try:
        with open (config_file, 'rb') as f:
            config = json.load(f)
    except:
        sys.stderr.write("Failed to load config.\n")
        sys.exit(1)

headers = {'User-Agent': config['UA'], 'Referer': config['referer']}

try:
    # Uploading picture
    r = www.post(config['url'] , data={'format':'json', 'key':config['key'], 'optimage':'0'}, files={'fileupload':(Filename, open(File, 'rb'))}, headers=headers)
    if r.ok:
        Data = r.json()
        Status = "http://img%s.imageshack.us/img%s/%s/%s" % (Data['files']['server'], Data['files']['server'], Data['files']['bucket'], Data['files']['image']['filename'])
    else:
        Status = r.status_code
except:
    Status = 'Error!'
    raise

print Status

# Popup notify
try:
    #run.check_output(['which', 'kdialog'])
    run.call(['kdialog', '--icon', 'ImageShack', '--passivepopup', Status, '3'])
except:
    try:
        #run.check_output(['which', 'notify-send'])
        run.call(['notify-send', '-t', '3000', '--icon=ImageShack', Status])
    except:
        pass
    raise

# Put link to the clipboard
if 'DISPLAY' in os.environ:
    try:
        xclip = run.Popen(['xclip'], stdin=run.PIPE)
        xclip.communicate(input=Status)
        xclip.terminate()
    except:
        pass
