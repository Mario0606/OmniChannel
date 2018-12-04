from tweepy.streaming import StreamListener

class listener(StreamListener):
    def on_data(self, data):
        return data
    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status, flush = True)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_error(self, status):
        print (status)
