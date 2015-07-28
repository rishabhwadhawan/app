from kafka import SimpleProducer, KafkaClient, KafkaConsumer
import mongo
import sys

sampleReqRespObjStr = """{"type":"GET", "url" : "http://localhost:8080/main",  "reqData" : "", "respData" : "" } """


KAFKA_TOPIC = 'validator'
KAFKA_GROUP = 'validatorgrp'
KAFKA_SERVER = 'localhost:9092'

IS_NG_PRESENT = False

class KafkaInterface:
    
    def __init__(self, *args, **kw):
        self.consumer = KafkaConsumer(KAFKA_TOPIC, group_id=KAFKA_GROUP,
                         bootstrap_servers=[KAFKA_SERVER])
        self.mongo = mongo.ValidatorTable()
    
    def consume(self):
	print "Consumer Running"
        for message in self.consumer:
            reqRespObStr = message.value
            print reqRespObStr
            self.mongo.insert_log(reqRespObStr)
            if IS_NG_PRESENT:
                    pass
#                  ApiValidator.validate(reqRespObStr)
    def produce(self, message):
	print "Produce:"
        kafka = KafkaClient(KAFKA_SERVER)
        producer = SimpleProducer(kafka)
        producer.send_messages(KAFKA_TOPIC, message)        
    
if __name__ == "__main__":
	ki = KafkaInterface()
	if len(sys.argv) > 1 and sys.argv[1] == "consume":
		ki.consume()
	else:
		ki.produce(sys.argv[2])
    
    
    


