import re
import os
import yaml
import pandas as pd

pkg_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(pkg_path, 'config.yml')
cfg = yaml.safe_load(open(config_path, 'r'))
cfg = type('Namespace', (object, ), cfg)


def remove_adjacent_duplicates(str):
    return re.sub(r'(.)\1+', r'\1\1', str)


def format_string(str):
    if str:
        locale_chars = ''
        if cfg.country_code == 'vn':
            locale_chars = ' ,.\n\tABCDEGHIKLMNOPQRSTUVXYabcdeghiklmnopqrstuvxyÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
        elif cfg.country_code == 'sg':
            locale_chars = ' ,.\n\tABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        bad_chars = [('\t', ', '), ('\n', '. '), ('  ', ' '), (' .', '.'),
                     (' ,', ','), ('..', '.'), (',,', ','), (',.', '.'),
                     ('.,', ',')]
        # Keep only specific characters
        str = ''.join(c for c in str if c in locale_chars)
        str = remove_adjacent_duplicates(str)
        for c in bad_chars:
            str = str.replace(c[0], c[1])
        str = str.strip()
    return str


def export_to_text_file(array_of_json,
                        product_info,
                        filename,
                        only_header=False):
    f = open(filename, 'a+', encoding='utf-8')
    if only_header:
        f.write(
            'userid\tshopid\titemid\tcmtid\tmtime\trating_star\tcomment\tproduct_name\tshop_name\tshop_rating\tavg_rating\trating_count\tsold\n'
        )
    else:
        for j in array_of_json:
            # print(';'.join(*product_info))
            f.write(
                '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                    j['userid'],
                    product_info['shopid'],
                    product_info['itemid'],
                    j['cmtid'],
                    j['mtime'],
                    j['rating_star'],
                    j['comment'],
                    product_info['product_name'],
                    product_info['shop_name'],
                    product_info['shop_rating'],
                    product_info['rating_star'],
                    product_info['rating_count'],
                    product_info['sold'],
                ))
    f.close()


def remove_duplicate_column(filename, col_check, filename_out=None):
    df = pd.read_csv(filename, delimiter='\t')
    print(df['rating_star'].value_counts().sort_index(ascending=True))
    df.drop_duplicates(col_check, inplace=True)
    print(df['rating_star'].value_counts().sort_index(ascending=True))
    filename_out = filename if filename_out is None else filename_out
    df.to_csv(filename_out, sep='\t', index=False)


def prune(filename):
    df = pd.read_csv(filename, delimiter='\t')
    min = df.groupby('rating_star').agg('count')['comment'].min()
    for i in [1, 2, 3, 4, 5]:
        rows = df.loc[df['rating_star'] == i]
        rows = rows.sort_values(by='comment',
                                key=lambda x: x.str.len(),
                                ascending=False)
        rows = rows.head(min)
        header = True if i == 1 else False
        rows.to_csv('pruned_' + filename,
                    mode='a',
                    index=False,
                    sep='\t',
                    header=header)
