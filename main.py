import csv 
import matplotlib.pyplot as plt
import datetime as dt
import sys
import numpy as np
from matplotlib import colors

START_DATE = dt.date(2017,8,1)
END_DATE = dt.date(2018,9,1)

def get_balance(entires):
	dates = [r[0] for r in entries]

	dates = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]
	balance = [float(r[7]) for r in entries]

	return dates, balance
	
def get_debit(entries):

	dates = [r[0] for r in entries]

	all_dates = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

	ys = []
	dates = []
	labels = []
	for i in range(len(entries)):
		try:
			ys = ys + [float(entries[i][5])]
			dates = dates + [all_dates[i]]
			labels = labels + [entries[i][4]]
		except:
			pass
	
	return dates, ys,labels

def get_credit(entries):


	dates = [r[0] for r in entries]

	all_dates = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

	ys = []
	dates = []
	labels = []
	for i in range(len(entries)):
		try:
			ys = ys + [float(entries[i][6])]
			dates = dates + [all_dates[i]]
			labels = labels + [entries[i][4]]
		except :
			pass
	
	return dates, ys,labels
	
def pie_chart(date_start, date_end,entries,chart_type="debit"):

	assert(date_start < date_end)
	dates = [r[0] for r in entries]

	dates = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

	pie = {}

	for entry in entries:


		date = dt.datetime.strptime(entry[0],'%d/%m/%Y').date()
		label = entry[4]
		failed = False
		try:
			if chart_type=="debit":
				value = float(entry[5])
			elif chart_type=="credit":
				value = float(entry[6])
			
		except:
			failed = True


		if failed == False and date >= date_start and date < date_end:

			if label in pie.keys():
					pie[label] = pie[label] + value 
			else:
				pie.update({label:value}) 

	return pie
		
def plot_monthly_pie_charts(entries,chart_type="debit"):

	start_date = START_DATE
	end_date = END_DATE
	increment = dt.timedelta(days=30)
	current_date = start_date + increment
	count = 0
	while current_date < end_date:

		print start_date,current_date
 		fig, ax = plt.subplots(1,figsize=(8*2,6*2))

		pie = pie_chart(date_start = start_date,date_end=current_date,entries =entries,chart_type=chart_type)
		tuples = sorted(zip(pie.keys(),pie.values()),key=lambda x: x[0])

		try:
			xs = [t[0] for t in tuples]
			ys =[t[1] for t in tuples]
			ax.bar(xs,ys)
			plt.setp(ax.xaxis.get_majorticklabels(), rotation=90 )
			plt.title("Spending in date range: {0} - {1} [Total in/out: {2} GBP]".format(start_date,current_date,np.sum(ys)))
			ax.minorticks_on()
			plt.grid(b=True, which='major', color='black', linestyle='-')
			plt.grid(b=True, which='minor', color='grey', linestyle='--')
			
			plt.tight_layout()

			plt.savefig("images/{0}_pie_charts/img_{1}.png".format(chart_type,count))
			fig.close()

		except:
			pass
		count = count + 1
		start_date = current_date
		current_date = current_date + increment


def plot_charts(entries):
	plot_monthly_pie_charts(entries,chart_type="debit")
	plot_monthly_pie_charts(entries,chart_type="credit")


if __name__ == "__main__":
	f = "statement_1.csv"
	with open(f,"r") as file:
		rows = [r for r in csv.reader(file,delimiter=",")]
		
		header = rows[0]
		print header
		entries = rows[1:]

		# plot_charts(enties)

		fig, axarr = plt.subplots(3,2,figsize=(8,6))
		dates, values, labels = get_debit(entries)
		axarr[0][0].plot(dates, values, 'x-')
		axarr[0][0].set_xlabel("Date")
		axarr[0][0].set_ylabel("Debit [GBP]")


		N,bins, patches = axarr[0][1].hist(values,bins=np.linspace(0,500,500),facecolor='green', alpha=0.75)
		fracs = N/N.max()
		norm = colors.Normalize(fracs.min(), fracs.max())
		for thisfrac, thispatch in zip(fracs, patches):
		    color = plt.cm.viridis(norm(thisfrac))
		    thispatch.set_facecolor(color)

		axarr[0][1].set_xlabel("Debit Transaction Amount [GBP]")
		axarr[0][1].set_ylabel("Frequency")
		axarr[0][1].set_xlim([0,100])


		dates, values, labels = get_credit(entries)
		axarr[1][0].plot(dates, values, 'x-')
		axarr[1][0].set_xlabel("Date")
		axarr[1][0].set_ylabel("Credit [GBP]")
		
		

		dates, values  = get_balance(entries)
		axarr[2][0].plot(dates, values, 'x-')
		axarr[2][0].set_xlabel("Date")
		axarr[2][0].set_ylabel("Balance [GBP]")

		plt.show()
