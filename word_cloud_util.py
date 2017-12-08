# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

from wordcloud import WordCloud
from PIL import Image, ImageSequence
import numpy as np

def gen_by_text(text, image_path=None, width=1000, height=1000, font_path=None, save_path='result.png'):
    '''
    直接分析text得到文本
    :param text:
    :param image_path:
    :param width:
    :param height:
    :param font_path:
    :param save_path:
    :return:
    '''
    # 保证text是unicode编码
    # text = text.decode('utf-8')
    if font_path is None:
        print 'wordcloud is not support chinese!!!'
    mask = None
    if image_path:
        image = Image.open(image_path)
        mask = np.array(image)
    wordcloud = WordCloud(font_path=font_path, mask=mask, width=width, height=height,
                              background_color="white")
    wordcloud.generate(text)
    wordcloud.to_file(save_path)

if __name__ == '__main__':
    text = '''
    中新社北京11月6日电 （记者 阮煜琳）6日，京津冀晋鲁豫6省市“2+26城市”联合启动的空气重污染橙色预警进入第3日。由于空气污染不同程度缓解，中国环境保护部6日下午表示，河北中部、山西南部、山东西部城市6日15时开始陆续解除预警。专家表示，各地及时启动重污染天气预警，严格落实减排措施，起到良好效果。   　　
环保部2日称，4日至8日，京津冀及周边地区会出现区域性重污染天气过程，其中6日可达此次污染过程峰值。3日，北京、天津和河北、山西、山东、河南等地部分城市陆续发布重污染天气橙色预警，从4日零时开始启动II级应急响应。环保部6日表示，4日，京津冀及周边地区空气质量总体为良-轻度污染，只有太原、保定等城市小时浓度达到中度污染级别。  　　“在污染累积前就把排放强度降下去，是重污染天气应急能否取得成效的关键”，中国科学院大气物理研究所研究员王自发6日说，有研究表明，提前1天-2天采取应急减排措施，能够更有效地降低PM2.5峰值浓度，推迟重污染发生的时间。因此，针对这次污染过程，各地提前发布预警信息，及时启动应急减排措施，及早防控。  　　这次污染过程中多地实际空气质量好于预测，对此，中国环境科学研究院研究员柴发合说，针对这次污染过程，京津冀及周边地区“2+26”城市采取了区域应急联动，强制性应急减排措施包括钢铁、水泥、铸造、家具、矿山开采等行业的停限产，国Ⅲ及以下的机动车限行，重点企业错峰运输，施工和交通扬尘管控等。  　　
同时，今年各地重污染天气应急预案大幅增加了管控企业数量，压实减排措施，基本做到涉气企业全覆盖。初步分析，京津冀及周边区域“2+26”城市在采取橙色预警期间，主要污染物减排比例在20%左右，有效抑制了此次污染过程中京津冀区域PM2.5浓度的快速上升。  　　“民众实际感受到的空气质量是地方政府已经采取应急减排措施后的结果，实际空气质量比预测的好，正说明已经采取的减排措施起到了一定效果”，柴发合说，由于现阶段京津冀及周边地区的产业结构和能源结构等因素，区域污染物排放量依然巨大，应急减排只能一定程度上减轻重污染的影响。  　　柴发合说，环保部派出的28个督查组和102个巡查组，共检查企业1085家。各地高度重视重污染天气应对工作，严格减排措施落实。使本次重污染天气过程影响降低了很多，污染浓度峰值比预测要低，持续时间也相对较短。  　　环保部表示，结合最新预报结果，已经发文指导各地分批错时解除橙色预警。河北中部、山西南部、山东西部城市可于6日15时解除预警，其他城市可于6日晚24时解除。
    '''.decode('utf-8')
    image = Image.open('resource/cloud.jpg')
    graph = np.array(image)
    wordcloud = WordCloud(font_path='resource/simkai.ttf', mask=graph, width=10000, height=1000, background_color="white")
    # wordcloud.generate_from_frequencies({u'词a': 100,u'词b': 10, u'词c': 50})
    wordcloud.generate(text)
    # width,height,margin可以设置图片属性

    # generate 可以对全部文本进行自动分词,但是他对中文支持不好,对中文的分词处理请看我的下一篇文章
    # wordcloud = WordCloud(font_path = r'D:\Fonts\simkai.ttf').generate(f)
    # 你可以通过font_path参数来设置字体集

    # background_color参数为设置背景颜色,默认颜色为黑色

    import matplotlib.pyplot as plt

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    wordcloud.to_file('resource/cloud_word_result.png')
    # 保存图片,但是在第三模块的例子中 图片大小将会按照 mask 保存
