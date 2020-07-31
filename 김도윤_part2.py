"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.

김도윤
"""

IDENTICAL = -1

#####################################################################
#                              PROBLEM1                             #
#####################################################################

def singleline_diff(line1, line2):
    if len(line1) < len(line2):
        shorterline = line1
    else:
        shorterline = line2    
    
    if line1 == line2:
        return IDENTICAL
    
    elif line1[:(len(shorterline))] == line2[:(len(shorterline))]: 
        return len(shorterline)
    
    else:
        n = 0
        for n in range(len(shorterline)):
            if line1[n] == line2[n]:
                n += 1
                
            elif line1[n] != line2[n]:
                return n
            
        # MSBAK
        # 29번 줄에서
        # for n in A: 일때, n은 A로 부터 자동으로 할당 받습니다.
        # 예를들어 A = list([1,2,3,4]) 일때 n은 1, 2, 3, 4를 순차적으로 받습니다.
        # 위의 구문을 보면 n += 1을 했네요. 의도한 바와는 다르게 코딩한것으로 생각됩니다.
        # print(list(range(len(shorterline)))) 를 실행해보거나
        # for n in range(len(shorterline)):
        #   print(n)
        # 을 해보면 더 이해하기 쉬울겁니다.
        
        # 26번 줄은 목적이 뭔지 잘 모르겟네요.
            

#####################################################################
#                              PROBLEM2                             #
#####################################################################

def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    ####여기에서 idx를 미리 정의하면 나중에 사용되지 않고 지역변수로 설정할 경우에는 line1, line2가 미리 설정되지 않아
    #### 오류가 유발되어 마지막에 idx를 singleline_diff함수를 이용해 표현하고 여기에서는 그냥 두었습니다
    
    
    if idx < 0:
        return ""
    
    elif line1.find("\n")!=-1 or line1.find("\r")!=-1 or line2.find("\n")!=-1 or line2.find("\r")!=-1:
        return ""
    
    else:
        indicator = "="*idx + "^"
        answer = line1 + "\n" + indicator + "\n" + line2    
        return answer

#####################################################################
#                              PROBLEM3                             #
#####################################################################

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """  
    
    if lines1 == lines2:
        return "(IDENTICAL, IDENTICAL)"
    
    else:
        line_no = singleline_diff(lines1, lines2)
                
        idx = singleline_diff(lines1[line_no], lines2[line_no])
        # MSBAK: 이러면 언제나 0이 나올것 같은데요?

        return (line_no, idx)

#####################################################################
#                              PROBLEM4                             #
#####################################################################

def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    datafile = open(filename, "rt")
    reading = datafile.read()
    reading.split(" ")
    
    datafile.close()

    return reading.split(". ")

    # .split은 처음보는 기능인데 찾아보니 \n 제거 목적을 위해 사용되는 함수네요.
    # 검색으로 기능을 찾아 써보는것은 아주 좋습니다.
    # 문제는 여전히 제거되지 않았고, 여러줄이 한줄로 입력되서 서로 다른 줄을 구별하기 힘드네요.
    # 입력받는것은 순수한 문법및 기능의 문제이니 외우면 됩니다. 정답지를 참고해보세요.
    
    



#####################################################################
#                              PROBLEM5                             #
#####################################################################

def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    if get_file_lines(filename1) == get_file_lines(filename2):
        return "No differences\n"
    
    else:
        
        list1 = get_file_lines(filename1)
        list2 = get_file_lines(filename2)
        
        diff = multiline_diff(list1, list2)
        
        # project description에는 이에 대한 설명이 따로 없는 것 같지만
        #split을 할 때 '.'를 기준으로 나누었기 때문에 원본을 다시 보여주고자 .를 추가했습니다
        
        diffline1 = list1[diff[0]] + "."
        diffline2 = list2[diff[0]] + "."
        
        show_diff = singleline_diff_format( diffline1, diffline2, diff[1])
        
        # line number은 0부터
        answer = "Line: " + str(diff[0]) + "\n" + show_diff
    
        return answer



print(file_diff_format("file2.txt", "file3.txt"))
list1 = get_file_lines("file2.txt")









