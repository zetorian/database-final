#!/usr/bin/python2                       
                                                                                                                                                                          
import os                                                                                 
import Cookie                                                                                                                                                             
                                                                                                                                                                          
print 'content-type: text/html\n'                                                                                                                                         
                                                                                                                                                                          
#here we need to set the user and type for the correct homepage of the logged in user                                                                                     
                                                                                                                                                                          
user=''                                                                                                                                                                   
userType='doctor'
userSSN=''
                                                                                                                                                                          
if userType=='doctor':                                                                                                                                                    
    print '<head> <meta http-equiv="Refresh" content="1; url=homeDoc.py"> </head>'                                                                                        
                                                                                                                                                                          
if userType=='nurse':                                                                                                                                                     
    print '<head> <meta http-equiv="Refresh" content="1; url=homeNurse.py"> </head>'                                                                                      
                                                                                                                                                                          
if userType=='patient':                                                                                                                                                   
    print '<head> <meta http-equiv="Refresh" content="1; url=homePatient.py"> </head>'                                                                                    
                                                                                                                                                                                                                                                                   
