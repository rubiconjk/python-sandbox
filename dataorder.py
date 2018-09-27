# This program will calcualte the number of sections of aerials and parcel
# data a customer is ordering (factoring in the data discount) and returns
# the appropriate charge.

print "\nGISMO Data Order Calculator v0.3"
print "Last modified: 9-19-2013\n\n"

numsections = int(raw_input("Enter number of sections requested: "))

print " "

numfree = numsections / 4       # Calculate the number of free sections.
numpay = numsections - numfree  # Calculate the number of paid sections.

aerialprice = 20 * numpay   # Calculate the charge for number of sections of aerials.
parcelprice = 50 * numpay   # Calculate the charge for number of parcels.
total = aerialprice + parcelprice   # Calculate the charge for both aerials and parcels.

print "Number of free sections will be:    %d" % (numfree)
print "Number of charged sections will be: %d" % (numpay)
print " "

if parcelprice >= 2500:
  print "Charge for parcels is $2,500.00"
  print "**Customer should order full parcel layer.**"
  
else:
  print "Charge for parcels is: $%.2f" % (parcelprice)

print "Charge for aerials is: $%.2f" % (aerialprice)
print " "
print " "

raw_input("Press Enter to exit")
