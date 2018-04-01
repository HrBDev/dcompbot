from mysql.connector import connection

cnx = connection.MySQLConnection(user=<Database,
                                 password=<Database Password>,
                                 host=<Host IP>,
                                 database=<Database name>,
                                 charset='utf8mb4')

def fetch_all(query):
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    if result is None:
        return False
    else:
        return result


def get_sections():
    query = """SELECT *
    FROM tbl_section
    WHERE active = TRUE
    ORDER BY position ASC;"""
    return fetch_all(query)


def get_section_name():
    query = """SELECT name
    FROM tbl_section
    WHERE active = TRUE
    ORDER BY position ASC;"""
    return fetch_all(query)


def get_id_section(id_section):
    query = """SELECT *
    FROM tbl_section
    WHERE active = TRUE
    AND id_section = {id_section}
    ORDER BY position ASC;""".format(id_section=id_section)
    return fetch_all(query)


def get_id(id_section, section):
    # query = "SELECT concat(id_section,0x2D,tbl_section.name) AS getId" + " FROM tbl_section" + " WHERE active = TRUE" + " AND tbl_section.name = \"" + section + "\" AND id_section = " + id_section
    query = """SELECT concat(id_section,0x2D,tbl_section.name) AS getId
    FROM tbl_section
    WHERE active = TRUE 
    AND tbl_section.name = \"{section} \" 
    AND id_section = {id_section}""".format(id_section=id_section, section=section)
    result = fetch_all(query)
    return result is not None


def get_id_option(id_option, id_field, option):
    query = """SELECT concat(id_option,0x2D,id_field,0x2D,tbl_option.name) AS getId
    FROM tbl_option
    WHERE active = TRUE
    AND id_option = {id_option}
    AND tbl_option.name = \"{option} \"
    AND id_field = {id_field}""".format(id_option=id_option, id_field=id_field, option=option)
    result = fetch_all(query)
    return result is not None


def get_id_content(id_content, id_option, content):
    query = """SELECT concat("1",0x2D,id_content,0x2D,id_option,0x2D,tbl_content.name) AS getId
    FROM tbl_content
    WHERE active = TRUE
    AND id_option = {id_option}
    AND tbl_content.name = \"{content} \"
    AND id_content = {id_content}""".format(id_option=id_option, id_content=id_content, content=content)
    result = fetch_all(query)
    return result is not None


def get_fields(id_section):
    query = """SELECT *
    FROM tbl_field
    WHERE id_section = {} AND active = TRUE
    ORDER BY position ASC;""".format(id_section)
    return fetch_all(query)


def get_options(id_field):
    query = """SELECT *
    FROM tbl_option
    WHERE id_field = {} AND active = TRUE
    ORDER BY position ASC;""".format(id_field)
    return fetch_all(query)


def get_content(id_option):
    query = """SELECT *
    FROM tbl_content
    WHERE id_option = {} AND active = TRUE
    ORDER BY position ASC;""".format(id_option)
    return fetch_all(query)


def get_content_filled(id_content):
    query = """SELECT *
    FROM tbl_content_fill
    WHERE id_content = {} AND active = TRUE
    ORDER BY position ASC;""".format(id_content)
    return fetch_all(query)


def get_content_filled_msg(id_content):
    query = """SELECT
  concat(tbl_section.name, 0x202d2d3e20, tbl_option.name, 0x202d2d3e20, tbl_content.name) AS name
FROM tbl_section
  INNER JOIN tbl_field ON tbl_section.id_section = tbl_field.id_section
  INNER JOIN tbl_option ON tbl_field.id_field = tbl_option.id_field
  INNER JOIN tbl_content ON tbl_option.id_option = tbl_content.id_option
WHERE tbl_content.id_content = {};""".format(id_content)
    return fetch_all(query)

def get_content_msg(id_option):
    query = """SELECT
  concat(tbl_section.name, 0x202d2d3e20, tbl_option.name, " ، درچه زمینه ای سوال دارید؟") AS name
FROM tbl_section
  INNER JOIN tbl_field ON tbl_section.id_section = tbl_field.id_section
  INNER JOIN tbl_option ON tbl_field.id_field = tbl_option.id_field
WHERE tbl_option.id_option =  {};""".format(id_option)
    return fetch_all(query)
