function timer()
           {
               var ts = (new Date(2019,10 , 1, 0, 0, 0)) - (new Date( ));//计算剩余的毫秒数
               var dd = parseInt(ts / 1000 / 60 / 60 / 24, 10);//计算剩余的天数
               var hh = parseInt(ts / 1000 / 60 / 60 % 24, 10);//计算剩余的小时数
               var mm = parseInt(ts / 1000 / 60 % 60, 10);//计算剩余的分钟数
               var ss = parseInt(ts / 1000 % 60, 10);//计算剩余的秒数
               dd = checkTime(dd);
               hh = checkTime(hh);
               mm = checkTime(mm);
               ss = checkTime(ss);
               document.getElementById("timer").innerHTML = dd + "天" + hh + "时" + mm + "分" + ss + "秒";
               setInterval("timer()",1000);      //注释此行，不进行倒计时显示
           }
           function checkTime(i)
           {
              if (i < 10) {
                  i = "0" + i;
               }
              return i;
           }
