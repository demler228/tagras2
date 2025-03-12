from utils.connection_db import connection_db
import psycopg2


class EducationDAL(object):
    @staticmethod
    def get_themes():
        conn = connection_db()

        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM themes
                """

                cursor.execute(query)
                themes = cursor.fetchall()

                return themes

        except Exception as e:
            print(str(e))
            return e

        finally:
            conn.close()

    @staticmethod
    def get_material(theme_id: int):
        conn = connection_db()

        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT title, url FROM materials WHERE theme_id = %s
                """

                cursor.execute(query, (theme_id,))
                materials = cursor.fetchall()

                return materials

        except Exception as e:
            print(str(e))
            return e

        finally:
            conn.close()

