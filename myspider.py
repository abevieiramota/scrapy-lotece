# -*- coding: utf-8 -*-
import scrapy
import re

PATH_DATAS = '//div[@class="dataResultado"]/div[@class="data branco"]/text()'
PATH_RESULTADOS = ('//div[@class="dataResultado"]/ul/li/'
                   'div[@class="numeros"]/text()')
RE_DATA_TURNO = re.compile(r'^.*?(\d{2}/\d{2}/\d{4})[\s-]*(.*)$')


class LoteceSpider(scrapy.Spider):
    name = 'lotece'
    start_urls = ['http://www.lotece.com.br/v2/?page_id=70']

    def parse(self, response):

        # extract results
        datas_turnos = response.xpath(PATH_DATAS).getall()
        datas = []
        turnos = []
        for data_turno in datas_turnos:

            data, turno = RE_DATA_TURNO.findall(data_turno)[0]
            datas.append(data)
            turnos.append(turno)

        resultados = response.xpath(PATH_RESULTADOS).getall()
        resultados = [r.strip() for r in resultados]

        for i in range(len(datas)):

            dado = dict(data=datas[i],
                        turno=turnos[i],
                        premio1=resultados[i*10],
                        premio2=resultados[i*10 + 1],
                        premio3=resultados[i*10 + 2],
                        premio4=resultados[i*10 + 3],
                        premio5=resultados[i*10 + 4],
                        premio6=resultados[i*10 + 5],
                        premio7=resultados[i*10 + 6],
                        premio8=resultados[i*10 + 7],
                        premio9=resultados[i*10 + 8],
                        premio10=resultados[i*10 + 9]
                        )

            yield dado

        yield response.follow(response.xpath(
                '//a[@class="pg"]/@href').getall()[-1],
                              self.parse)
