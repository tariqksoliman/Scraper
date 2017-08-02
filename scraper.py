# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen, URLError
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

fileName = "Output.txt"
url = 'http://www.novel99.com/words-radiance-stormlight-archive-2-brandon-sanderson'
urlAppend = '?page=0,'
urlPageNum = 0;
chapterNum = 1;

#Clear the file
text_file = open( fileName, 'w' ).close()

for u in range( 0, 514 ):
    
    req = Request( url + urlAppend + str(urlPageNum), headers=hdr )

    try:
        response = urlopen( req )
        soup = BeautifulSoup( response.read().decode( 'utf-8', 'ignore' ), 'html.parser' )

        pageText = soup.find( 'div', attrs={'class':'content'} ) 
        pageText.find( 'div', attrs={'class':'links'} ).extract()
        pageText = pageText.findAll( text=True )

        pageText = pageText[1:]
        pageText = pageText[:-2]

        i = 0;
        for pg in pageText:
            if u'\u2014' == pg[0]:
                pageText.insert( i + 1, '\n-- ' + str( chapterNum ) + ' --\n' )
                i += 1
                chapterNum += 1
            i += 1
        pageTextStr = "".join([ (item) for item in pageText ])

        text_file = open( fileName, 'a' )
        text_file.write( pageTextStr.encode( 'utf-8' ) )
        text_file.close()

        urlPageNum += 1

    except URLError as e:
        if hasattr( e, 'reason' ):
            print 'Failed to reach a server.'
            print 'Because: ', e.reason
        elif hasattr( e, 'code' ):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code