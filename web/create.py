import os
import config
import datetime
import json
import overview
import update


def doIt( tlId, environ, start_response ) :
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")  
    print ("Creating workdown "+ tlId + ", filename will be " + config.WODODIR+"/"+tlId+"."+dt+".json")
    # print ("TALIDIR: "+config.TALIDIR+", WODODIR: "+config.WODODIR)
    
    lines = []
    with open(config.TALIDIR+"/"+tlId+".json") as json_file:
        jason_data = json.load(json_file)
    jason_data["workdown_created"] = datetime.datetime.now().strftime('%Y/%m/%d %H-%M-%S')
    jason_data = update.count_results(jason_data)
    # jason_data["workdown_last_updated"] = None
        
    if not os.path.isdir( config.WODODIR+"/"+os.path.split(tlId)[0] ):
        os.makedirs(config.WODODIR+"/"+os.path.split(tlId)[0])
        
    with open(config.WODODIR+"/"+tlId+"."+dt+".json", 'w') as fp:
        json.dump(jason_data, fp, indent=4)

    start_response('303 See Other', [('Location',config.CONTEXT+'/render/'+tlId+"."+dt)])

    return ['1']
