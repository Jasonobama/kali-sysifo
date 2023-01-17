import os
import time
import logging

# Return CPU temperature as a character string                                     
def  getCPUtemperature():
     file =  open("/sys/class/thermal/thermal_zone0/temp")
     temp = float(file.read()) / 1000
     file.close()
     return(temp)

# Return RAM information (unit=kb) in a list                                      
# Index 0: total RAM                                                              
# Index 1: used RAM                                                                
# Index 2: free RAM                                                                
def  getRAMinfo():
     p  = os.popen( 'free' )
     i  = 0
     while  1 :
         i  = i  + 1
         line  = p.readline()
         if  i == 2 :
             return (line.split()[ 1 : 4 ])
 
# Return % of CPU used by user as a character string                               
def  getCPUuse():
     return ( str (os.popen( "top -n1 | awk '/Cpu\(s\):/ {print $2}'" ).readline().strip()))
 
# Return information about disk space as a list (unit included)                    
# Index 0: total disk space                                                        
# Index 1: used disk space                                                        
# Index 2: remaining disk space                                                    
# Index 3: percentage of disk used                                                 
def  getDiskSpace():
     p = os.popen( "df -h /" )
     i = 0
     while 1 :
         i  = i  + 1
         line  = p.readline()
         if i == 2 :
             return (line.split()[ 1 : 5 ])

def get_info():
     
     # CPU informatiom
     CPU_temp  = getCPUtemperature()
     CPU_usage  = getCPUuse()
     
     # RAM information
     # Output is in kb, here I convert it in Mb for readability
     RAM_stats  = getRAMinfo()
     RAM_total  = round ( int (RAM_stats[ 0 ])  / 1024 , 1 )
     RAM_used  = round ( int (RAM_stats[ 1 ])  / 1024 , 1 )
     RAM_free  = round ( int (RAM_stats[ 2 ])  / 1024 , 1 )
     
     # Disk information
     DISK_stats  = getDiskSpace()
     DISK_total  = DISK_stats[0]
     DISK_used  = DISK_stats[1]
     DISK_left = DISK_stats[2]
     DISK_perc  = DISK_stats[3]
     
     logging.info(
          "Local Time {timenow} \n"
          "CPU Temperature = {CPU_temp}'C \n"
          "CPU Use = {CPU_usage} %\n\n"
          "RAM Total = {RAM_total} MB\n"
          "RAM Used = {RAM_used} MB\n"
          "RAM Free = {RAM_free} MB\n\n"
          "DISK Total Space = {DISK_total}B\n"
          "DISK Used Space = {DISK_used}B\n"
          "DISK Left Space = {DISK_left}B\n"
          "DISK Used Percentage = {DISK_perc}\n"
          "".format(
               timenow = time.asctime(time.localtime(time.time())),
               CPU_temp = CPU_temp,
               CPU_usage = CPU_usage,
               RAM_total = str(RAM_total),
               RAM_used = str(RAM_used),
               RAM_free = str(RAM_free),
               DISK_total = str(DISK_total),
               DISK_used = str(DISK_used),
               DISK_left = str(DISK_left),
               DISK_perc = str(DISK_perc),
               )
     )

if __name__  == '__main__':
     # get info
     logger_file = os.path.join('log_source_info.txt')
     handlers = [logging.FileHandler(logger_file, mode='w'),
                logging.StreamHandler()]
     logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] '
                           '- %(levelname)s: %(message)s',
                           level=logging.INFO,
                           handlers=handlers)
     # while(1):
     while(True):
          get_info()
          time.sleep(10) # Time interval for obtaining resources
          os.system('clear') # Clear the terminal
