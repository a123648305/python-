from datetime import datetime, timedelta

def calculate(rate = 3,number = 456321.68):
    benPay = 2064.77
    # benPay = 2073
    now = datetime.now()
    monthRate =  rate * 0.01  / 12 
    addMonth = 0
    curMoney = number
    totalPay = 0
    totalInterest = 0
    totalBenPay = 0

    result = []


    while curMoney > 0:
        monthInterest = curMoney * monthRate
        totalInterest += monthInterest
        addMonth += 1
        if curMoney < benPay:
            monthPay = monthInterest + curMoney
            totalPay += monthPay
            totalBenPay += curMoney 
            res = f"{calcMonth(now,addMonth)} 剩余本金：{0:.4f} 累计本金：{totalBenPay:.4f} 累计利息：{totalInterest:.4f} 月本金：{curMoney:.4f} 月利息：{monthInterest:.4f} 月供款：{monthPay:.4f} 第{addMonth}期"
            result.append(res)
            break
        else:
            monthPay = monthInterest + benPay
            curMoney = curMoney - benPay
            totalPay += monthPay
            totalBenPay += benPay
            res = f"{calcMonth(now,addMonth)} 剩余本金：{curMoney:.4f} 累计本金：{totalBenPay:.4f} 累计利息：{totalInterest:.4f} 月本金：{benPay:.4f} 月利息：{monthInterest:.4f} 月供款：{monthPay:.4f} 第{addMonth}期"
            result.append(res)

    result.insert(0,f"总本金：{number} 年化利率：{rate}% 总共{addMonth}期")
    
    with open('利息.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))



def calcMonth(now,addMonth = 1):
    days = (addMonth-1) * 30
    future_time = now + timedelta(days)
    dayStr = future_time.strftime('%Y-%m')
    return dayStr



print('执行----')
# number = int(input('请输入本金：'))
rate = float(input('请输入年化利率：'))

calculate(rate)

print('执行完成')