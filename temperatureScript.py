import os
import subprocess

# filenames for recording the temps of the different GPUs, in the order 
# they appear in nvidia-smi
fnames = ['P40temp_2secondIncrements_normalBNNtraining']

def get_temps():
  s = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE)
  l = str(s.stdout).split('\\n')
  breakLineInds = []
  for i in range(len(l)):
    if l[i][0:4] == '+---':
      breakLineInds.append(i)
  pastTempBreak = min([ind for ind in breakLineInds if ind > 8])
  temps = []
  for line in l[8:pastTempBreak]:
    for item in line.split():
      if item[-1] == 'C': # Only the temp will pass this test
        temps.append(int(item[:-1]))
  return temps

def record_temp(fname, temp):
  s = str(temp)
  if os.path.exists(fname):
    s = ',' + s # appending to a comma-separated array
  f = open(fname, 'a')
  f.write(s)
  f.close()
  return 0

def main():
  temps = get_temps()
  M = min(len(temps), len(fnames))
  for i in range(M):
    record_temp(fnames[i], temps[i])
    print(fnames[i] + ':\t\t' + str(temps[i]))
  return 0

# Timing can be added here, or inherited from the 'watch' linux function
if __name__ == '__main__':
  main()
