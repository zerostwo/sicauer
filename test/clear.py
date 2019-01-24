import re


def course_info_clear(text):
    init = re.findall('(.+?)<br/>', re.findall('width="13.5%">(.+?)</td>', text)[0])
    c = '--------------------'
    if len(init) != 0:
        count = init.count(c)
        p = init.index(c)
        if count != 1:
            for i in init:
                init[init.index(i)] = re.sub('<(.+?)>', ' ', i)
            course1 = init[:p]
            course2 = init[p + 1:-1]
            course_info = {
                1: {
                    'course': course1[0],
                    'location': course1[1],
                    'time': course1[2],
                    'experiment': True if len(course1) == 4 else False
                },
                2: {
                    'course': course2[0],
                    'location': course2[1],
                    'time': course2[2],
                    'experiment': True if len(course2) == 4 else False
                }
            }
        else:
            for i in init:
                init[init.index(i)] = re.sub('<(.+?)>', ' ', i)
            course1 = init[:p]
            course_info = {
                1: {
                    'course': course1[0],
                    'location': course1[1],
                    'time': course1[2],
                    'experiment': True if len(course1) == 4 else False
                }
            }
    else:
        course_info = {}
    return course_info


if __name__ == '__main__':
    a = '<td align="center" height="50" valign="top" width="13.5%"> </td>'
    course_info_clear(a)
