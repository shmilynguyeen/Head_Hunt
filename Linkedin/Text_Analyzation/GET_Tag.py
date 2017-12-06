import nltk
from nltk.corpus import treebank
import MyConnection


class Get_Tag(): 


    li_Exe = {}
    def insertDB (self , key , tag , exe_ID , URL ) : 
        try : 
            sQuery = """ INSERT INTO [dbo].[Linkedin_Experience_Tag]
            ([Exp_Header_Id]
            ,[URL]
            ,[Tag]
            ,[Tag_Type])
        VALUES (?,?,?,?)""" 
            value = [exe_ID , URL , key  , tag]
            MyConnection.insertUpdateDB(sQuery , value)
            print("INSERT DONE ! ")
        except Exception as e : 
            print("INSERT ERROR ! " , e)

    def updateDB(self, exe_ID ) : 
        try : 
            sQuery = """ UPDATE   [LinkedIn_Experience_Header] SET [Is_Crawl] = 1 WHERE [Exp_Header_Id] = ? """
            value = [exe_ID]
            MyConnection.insertUpdateDB(sQuery , value)
            print ("UPDATE DONE ! ")
        except Exception as e : 
            print("UPDATE ERROR ! " , e)

    def main (self):
        sQuery = """ SELECT [Exp_Header_Id] , [Experience_Description], [URL] FROM [LinkedIn_Experience_Header]
         WHERE [Is_Crawl] IS NULL AND len([Experience_Description]) >2  """ 
        conn = MyConnection.getConnection()
        cursor = conn.cursor()
        cursor.execute(sQuery)
        result  = cursor.fetchone()
        while result : 
            # GET exe_ID & exe_Description !
            exe_ID = result[0]
            sentence = result[1]
            url = result[2]

            # Solving data ! 
            temp = sentence.split('-')
            
            for x in temp : 
                if ( len(x)  > 5 ) :  # Loại bỏ trường hợp bị null ! 
                    x = x.replace(',' , '')
                    x = x.replace('(' , '')
                    x = x.replace (')' , '')
                    x = x.replace('.', '')
                    x = x.replace('*' , '')
                    x = x.replace('#' , '')
                    tokens = nltk.word_tokenize(x)
                    tagged = nltk.pos_tag(tokens)
                    entities = nltk.chunk.ne_chunk(tagged)
                    # print(entities) 
                    for y in entities :
                        a1 = ""
                        a2 = ""
                        if (1 == len(y)): 
                            a = str(y)
                            a = str(y).replace('(' , '')
                            a= a.replace(')' , '')
                            a= a.replace("'" , "")
                            a= a.replace(',' , '')
                            a = a.split()
                            a2 = a[1]
                            a_temp  = a2.split('/')
                            a1 = a_temp[0]
                            a2 = a_temp[1]

                             
                        if(len(y)> 2): 
                            for i in y : 
                                a = ' '.join(i[0 : len(i)])
                                a = a.split()
                                a1 = a[0]
                                a2 = a[1]
                                # print(a1 , a2)
                                 
                        if (2 == len(y) ):     
                            a = str(y).replace('(' , '')
                            a=a.replace(')' , '')
                            a=a.replace("'" , "")
                            a= a.replace(',' , '')
                            a = a.split()
                            a1 = a[0]
                            a2 = a[1]
                        if (len(a1) > 1):
                            self.insertDB(a1 , a2, exe_ID , url)  
                        self.updateDB(exe_ID)
                        
            result = cursor.fetchone()
        conn.close()
        



if __name__ == "__main__" : 
    getTag = Get_Tag()
    getTag.main()

