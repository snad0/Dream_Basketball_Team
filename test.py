import pandas as pd
import pandasql as ps
Players = pd.read_csv('Players.csv')
SeasonsStats = pd.read_csv('Seasons_Stats.csv')
PlayerData = pd.read_csv('player_data.csv')

#first i checked for any null value and then cleaned the tables
PlayerData=PlayerData.dropna()
SeasonsStats=SeasonsStats.fillna("")

#here i've selected only those columns from SeasonsStats table which are usefull for my work
Data=ps.sqldf(""" SELECT  Player,Pos, Age,G,PTS
             FROM SeasonsStats
            
         """)
#here i joined both the tables and created career Goals and Career points columns which is sum or goals/points player have made in his entire career throughout the years
res=ps.sqldf("""
            SELECT name,Pos,Age,SUM(s.G) AS CareerGs, SUM(s.PTS) AS CareerPoints
            FROM PlayerData 
            LEFT JOIN Data AS s
            ON name = s.Player
            GROUP BY name
            ORDER BY CareerPoints DESC 
         """)

#now i have taken performance as CareerPoints/CareerGs to rank these players in the end acc to their performance and age
Data=ps.sqldf(""" SELECT *,CareerPoints/CareerGs AS Performance
             FROM res
            
         """) 
Data=Data.dropna()
result=ps.sqldf(""" SELECT *
             FROM( select *, Dense_rank() over(partition by POS order by Performance desc,Age asc)as rnk from Data) e where e.rnk<100 order by Performance desc             
            
        """)

# here i've taken performance whhich is Career Points divided by Career Goals as input criteria

X=int(input("Enter the Credits: \nMax Credits=100..."))
inp=X/5

rt=ps.sqldf(f""" SELECT  name as player_name, Pos as Position
             FROM result
             WHERE Performance< {inp}
             group by Pos
             limit 5


        """)

print(f"\n\nThe Best Players You Can Afford in {X} credits are:\n{rt}")