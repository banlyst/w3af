'''
wsdlFinder.py

Copyright 2006 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''

import core.controllers.outputManager as om
# options
from core.data.options.option import option
from core.data.options.optionList import optionList

from core.controllers.basePlugin.baseDiscoveryPlugin import baseDiscoveryPlugin
import core.data.kb.knowledgeBase as kb
import core.data.parsers.urlParser as urlParser
import core.data.parsers.wsdlParser
from core.controllers.w3afException import w3afRunOnce, w3afException

class wsdlFinder(baseDiscoveryPlugin):
    '''
    Find web service definitions files.
    
    @author: Andres Riancho ( andres.riancho@gmail.com )
    '''

    def __init__(self):
        baseDiscoveryPlugin.__init__(self)
        self._tested = []
    
    def discover(self, fuzzableRequest ):
        '''
        If url not in _tested, append a ?wsdl and check the response.
        
        @parameter fuzzableRequest: A fuzzableRequest instance that contains (among other things) the URL to test.
        '''
        self._fuzzableRequests = []
        self.is404 = kb.kb.getData( 'error404page', '404' )
        url = urlParser.uri2url( fuzzableRequest.getURL() )
        if url not in self._tested:
            self._tested.append( url )
            for wsdl in self._getWsdl():
                targs = (url , wsdl )
                self._tm.startFunction( target=self._get_wsdl, args=targs, ownerObj=self )
        self._tm.join( self )
        return self._fuzzableRequests

    def _get_wsdl( self, url, wsdl ):
        url2test = url + wsdl
        try:
            response = self._urlOpener.GET( url2test, useCache=True )
        except w3afException,  w3:
            om.out.debug('Failed to request the WSDL file: ' + url2test)
        else:
            # The response is analyzed by the wsdlGreper plugin
            pass
        
    
    def _getWsdl( self ):
        res = []
        
        res.append( '?wsdl' )
        res.append( '?WSDL' )
        
        return res
        
    def getOptions( self ):
        '''
        @return: A list of option objects for this plugin.
        '''    
        ol = optionList()
        return ol
        
    def setOptions( self, OptionList ):
        '''
        This method sets all the options that are configured using the user interface 
        generated by the framework using the result of getOptions().
        
        @parameter OptionList: A dictionary with the options for the plugin.
        @return: No value is returned.
        ''' 
        pass

    def getPluginDeps( self ):
        '''
        @return: A list with the names of the plugins that should be runned before the
        current one.
        '''
        return ['grep.wsdlGreper']
    
    def getLongDesc( self ):
        '''
        @return: A DETAILED description of the plugin functions and features.
        '''
        return '''
        This plugin finds new web service descriptions and other web service related files
        by appending "?WSDL" to all URL's and checking the response.
        '''
