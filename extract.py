import wave #sys, thread, time, traceback, Queue, os,
import os
import glob
import pymedia.muxer as muxer
import pymedia.audio.acodec as acodec

root= 'C:/Users/Silent/Downloads/Compressed/enterface database/'
root_vid= root+'enterface video/'
root_aud= root+'enterface audio/'

def convertToAudio(videopath,videoname):
    folder = root_vid + videopath
    vidName = videoname
    vidF= open(folder + vidName,'rb') #menu.cache.open( self.playingFile )

    format= vidName.split('.')[-1].lower() #menu.cache.getExtension( self.playingFile ) - probably just 'mpg', 'avi', etc...

    print "Source file:",vidName[vidName.rfind("\\")+1:]
    print "Format:",format

    dm= muxer.Demuxer( format )
    s = vidF.read( 300000 )
    r = dm.parse( s )
    #print dm.streams

    ac = None

    acFound = 0

    # Setup audio( only first matching stream will be used )
    for aindex in xrange( len( dm.streams )):
      if dm.streams[ aindex ][ 'type' ]== muxer.CODEC_TYPE_AUDIO:
        ac = acodec.Decoder(  dm.streams[ aindex ] )
        acFound = 1
        break

    if acFound == 1:

      #print ac,aindex

      write_string = '' # write all of the audio data to this string
      numErrors = 0

      while len(s):
        for d in r:
          if d[ 0 ] == aindex:
            try:
            #if True:
              afr = ac.decode( d[ 1 ] )
              snddata = afr.data

              # write the raw data if we have it
              if len( snddata )> 0:
                write_string = write_string + str(snddata)
            except:
              numErrors += 1

        s = vidF.read( 400000 )
        r = dm.parse( s )

      if numErrors > 0: print "Number of Errors:", numErrors

      if len(write_string) > 0:
        wavName = vidName.split('.')[0] + '.wav'

        if(not os.path.isdir(root_aud+videopath)):
            os.makedirs(root_aud + videopath)
        wavF = wave.open(root_aud+videopath + wavName,"wb")

        sampwidth = 2 # min(2,afr.bitrate/afr.sample_rate) # measured in bytes, not bits

        # set playback information
        wavF.setsampwidth(sampwidth)
        wavF.setframerate(afr.sample_rate)

        wavF.setnchannels(afr.channels)
        wavF.setcomptype('NONE','')

        num_frames = len(write_string)
        wavF.setnframes(num_frames)

        wavF.writeframes(write_string)
        wavF.close()
        """print ""
        print "Audio extracted successfully to", wavName
        print "Sample rate:",afr.sample_rate
        print "# of channels:",afr.channels
        print "Bitrate:",afr.bitrate
        print "Est. sample size:",sampwidth
        print "Est. duration",num_frames/(float(afr.sample_rate)*sampwidth*float(afr.channels))
        """
    else:
      print "no audio codec was selected"
    vidF.close()