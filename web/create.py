import os
import config
import datetime
import json
import overview


def doIt( tlId, environ, start_response ) :
    # response_headers = [('Content-type','text/html')]
    # start_response( '200 OK', response_headers)

    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")  
    print ("Creating workdown "+ tlId + ", filename will be " + config.WODODIR+"/"+tlId+"."+dt+".json")
    print ("TALIDIR: "+config.TALIDIR+", WODODIR: "+config.WODODIR)
    # shutil.copy( config.TALIDIR+"/"+tlId+".json", config.WODODIR+"/"+tlId+"."+dt+".json" )
    
    lines = []
    with open(config.TALIDIR+"/"+tlId+".json") as json_file:
        jason_data = json.load(json_file)
    jason_data["workdown_created"] = datetime.datetime.now().strftime('%Y/%m/%d %H-%M-%S')
    
    if not os.path.isdir( config.WODODIR+"/"+os.path.split(tlId)[0] ):
        os.makedirs(config.WODODIR+"/"+os.path.split(tlId)[0])
        
    with open(config.WODODIR+"/"+tlId+"."+dt+".json", 'w') as fp:
        json.dump(jason_data, fp, indent=4)

    # return overview.doIt( environ, start_response )
    # return 'Location: '+config.CONTEXT
    start_response('303 See Other', [('Location','http://google.com')])
    start_response('303 See Other', [('Location',config.CONTEXT+'/render/'+tlId+"."+dt)])

    return ['1']
