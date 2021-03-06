#!/usr/bin/python
import sys
import parts

sep = "    :"

def process(fh, results, debug=False, logfile=sys.stderr):
    """
    fh: file handle;
    results: dict for results;
    
    we assume mapblock.process() has already been run
    """
    bname = "SupParams"
    hsize = len(bname) + 1 # include trailing '\0'
    pname = "SupParams.process():"
    ref = None
    status = 'nok'
    
    try:
        ref = results['blocks'][bname]
        startpos = ref['pos']
        fh.seek( startpos )
    except:
        print >>logfile, pname," ",bname,"block starting position unknown"
        return status
    
    format = results['format']
    
    if format == 2:
        mystr = fh.read(hsize)
        if mystr != bname+'\0':
            print >>logfile, pname," incorrect header ",mystr
            return status
    
    results[bname] = dict()
    xref = results[bname]
    
    # version 1 and 2 are the same
    status = process_genparam(fh, results, debug=debug, logfile=logfile)
    
    # read the rest of the block (just in case)
    endpos = results['blocks'][bname]['pos'] + results['blocks'][bname]['size']
    fh.read( endpos - fh.tell() )
    status = 'ok'
    return status

# ================================================================
def process_genparam(fh, results, debug=False, logfile=sys.stderr):
    """ process SupParams fields """
    bname = "SupParams"
    xref  = results[bname]
    
    fields = (
              "supplier", # ............. 0
              "OTDR", # ................. 1
              "OTDR S/N", # ............. 2
              "module", # ............... 3
              "module S/N", # ........... 4
              "software", # ............. 5
              "other", # ................ 6
             )
    
    count = 0
    for field in fields:
        xstr = parts.get_string(fh)
        if debug:
            print >>logfile, "%s %d. %s: %s" % (sep, count, field, xstr)
        
        xref[field] = xstr
        count += 1
    
    status = 'ok'
    
    return status

