#  Required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
import json

#  Get the response of a carrer or school.
#  This code will try 5 time to requests the URL, this is because sometime the cloudscraper library returns an error.
print('Busca las escuela en: https://platzi.com/cursos/')
url = input('Ingrese la URL de la Carrera o Escuela:')
print('URL:', url)

attempt = 1
while attempt <= 5:
    try:
        scraper = cloudscraper.CloudScraper()
        r = scraper.get(url)
        s = BeautifulSoup(r.text, 'lxml')
        #  Start getting the info
        print('Obteniendo los siguientes datos de la ruta: Titulo de etapa, Nivel, Nombre del curso y link del curso ...')
        routes_content = s.find('div', attrs={'class': 'RoutesContent-content'})
        routes_list = routes_content.find_all('div', attrs={'class': 'RoutesList'})
        Dic_Route = {
            'Route_Name': [],
            'Title': [],
            'Level': [],
            'Course': [],
            'Link': []
        }
        route_name = s.find('div', attrs={'class': 'Hero-route-title'}).get_text()
        route_name_to_excel = route_name.lower().replace('.', '_').replace(' ', '_')
        for route in routes_list:
            title = route.find('h3', attrs={'class': 'RoutesList-title'}).get_text()
            level = route.find('div', attrs={'class': 'RoutesList-level'}).find('span').get_text()
            #  List of courses
            routes_list_items = route.find('div', attrs={'class': 'RoutesList-items'}).find_all('a', attrs={'class': 'RoutesList-item'})
            for course in routes_list_items:
                link = 'https://platzi.com' + str(course.get('href'))
                course_name = course.find('h4', attrs={'class': 'RoutesList-item-name'}).get_text()
                #  Add elements into Dic_Route
                Dic_Route['Route_Name'].append(route_name)
                Dic_Route['Title'].append(title)
                Dic_Route['Level'].append(level)
                Dic_Route['Course'].append(course_name)
                Dic_Route['Link'].append(link)
        Dic_Route_pd = pd.DataFrame(Dic_Route)
        print('Se obtuvo la información correctamente.')
        detail_input = input('¿Deseas obtener información detallada por cada curso? (Esto puede tardara unos minutos)\nIngresa el número:\n0 - No\n1 - Sí')
        if detail_input == '0' or detail_input == 0:
            Dic_Route_pd.to_excel(f'{route_name_to_excel}.xlsx', sheet_name='General_Info')
            print('Se guardo el excel correctamente.')
        else:
            print('Empezando a obtener información detallada...')
            Dic_Details_Course = {
                'Course': [],
                'Teacher': [],
                'Hours of study': [],
                'Hours of practice': [],
                'Quantity of classes': [],
                'Avg min/class': [],
                'Link': []
            }
            total_time_study = 0
            total_time_prtce = 0
            total_qutny_clss = 0
            #  Requests per course
            for course in Dic_Route_pd.itertuples():
                attempt_c = 1
                while attempt_c <= 5:
                    try:
                        r = scraper.get(course.Link)
                        s = BeautifulSoup(r.text, 'lxml')
                        #  Get info
                        teacher = s.find('h3', attrs={'class': 'TeacherDetails-name'}).get_text()
                        resources_schedule = s.find('ul', attrs={'class': 'ResourcesSchedule'}).find_all('p', attrs={'class': 'ResourcesSchedule-text'})
                        #  Time
                        try:
                            time_study = resources_schedule[0].find('span').get_text()
                            time_study_int = int(time_study.replace(' ', '').replace('Horas', '').replace('Hora', ''))
                        except:
                            time_study_int = 0
                        try:
                            time_prcte = resources_schedule[1].find('span').get_text()
                            time_prcte_int = int(time_prcte.replace(' ', '').replace('Horas', '').replace('Hora', ''))
                        except:
                            time_prcte_int = 0
                        content_classes = s.find('div', attrs={'class': 'Content-feed'}).find_all('li')
                        number_classes = len(content_classes)
                        avg = float(round((time_study_int*60/number_classes),2))
                        Dic_Details_Course['Course'].append(course.Course)
                        Dic_Details_Course['Teacher'].append(teacher)
                        Dic_Details_Course['Hours of study'].append(time_study_int)
                        total_time_study += time_study_int
                        Dic_Details_Course['Hours of practice'].append(time_prcte_int)
                        total_time_prtce += time_prcte_int
                        Dic_Details_Course['Quantity of classes'].append(number_classes)
                        total_qutny_clss += number_classes
                        Dic_Details_Course['Avg min/class'].append(avg)
                        Dic_Details_Course['Link'].append(course.Link)
                        print(f'{course.Course}: Correcto')
                        break
                    except Exception as err:
                        if attempt_c == 5:
                            print(f'{course.Course}: Fallido - Error: {err}')
                    attempt_c += 1
            Dic_Details_Course['Course'].append('TOTAL')
            Dic_Details_Course['Teacher'].append(' ')
            Dic_Details_Course['Hours of study'].append(total_time_study)
            Dic_Details_Course['Hours of practice'].append(total_time_prtce)
            Dic_Details_Course['Quantity of classes'].append(total_qutny_clss)
            Dic_Details_Course['Avg min/class'].append(' ')
            Dic_Details_Course['Link'].append(' ')
            
            Dic_Details_Course_df = pd.DataFrame(Dic_Details_Course)
            with pd.ExcelWriter(f'{route_name_to_excel}.xlsx') as writer:  
                Dic_Route_pd.to_excel(writer, sheet_name='General_Info')
                Dic_Details_Course_df.to_excel(writer, sheet_name='Detailed_Courses')
        print('Obtención detallada de cursos finalizada.')
        break
    except Exception as err:
        if attempt == 5:
            print(f'Error obteniendo información del servidor. Por favor intente de nuevo. Error: {err}')
    attempt += 1
