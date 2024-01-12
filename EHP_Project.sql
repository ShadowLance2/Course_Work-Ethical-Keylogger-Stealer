PGDMP                 	         |            EHP_Project    15.5    15.1 .    (           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            )           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            *           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            +           1262    43736    EHP_Project    DATABASE     �   CREATE DATABASE "EHP_Project" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "EHP_Project";
                postgres    false            �            1255    43840    audit_keylogs_delete_trigger()    FUNCTION     �   CREATE FUNCTION public.audit_keylogs_delete_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO audit_keylogs (date_time, record_id, what_done)
    VALUES (CURRENT_TIMESTAMP, OLD.keylog_id, 'DELETION');
    RETURN OLD;
END;
$$;
 5   DROP FUNCTION public.audit_keylogs_delete_trigger();
       public          postgres    false            �            1255    43838    audit_keylogs_trigger()    FUNCTION     �   CREATE FUNCTION public.audit_keylogs_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO audit_keylogs (date_time, record_id, what_done)
    VALUES (CURRENT_TIMESTAMP, NEW.keylog_id, 'INSERTION');
    RETURN NEW;
END;
$$;
 .   DROP FUNCTION public.audit_keylogs_trigger();
       public          postgres    false            �            1255    43839    audit_keylogs_update_trigger()    FUNCTION     �   CREATE FUNCTION public.audit_keylogs_update_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO audit_keylogs (date_time, record_id, what_done)
    VALUES (CURRENT_TIMESTAMP, NEW.keylog_id, 'UPDATE');
    RETURN NEW;
END;
$$;
 5   DROP FUNCTION public.audit_keylogs_update_trigger();
       public          postgres    false            �            1255    43846     audit_passwords_delete_trigger()    FUNCTION       CREATE FUNCTION public.audit_passwords_delete_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO audit_passwords (date_time, record_id, what_done)
    VALUES (CURRENT_TIMESTAMP, OLD.password_id, 'DELETION');
    RETURN OLD;
END;
$$;
 7   DROP FUNCTION public.audit_passwords_delete_trigger();
       public          postgres    false            �            1255    43844    audit_passwords_trigger()    FUNCTION     �   CREATE FUNCTION public.audit_passwords_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO audit_passwords (date_time, record_id, what_done)
    VALUES (CURRENT_TIMESTAMP, NEW.password_id, 'INSERTION');
    RETURN NEW;
END;
$$;
 0   DROP FUNCTION public.audit_passwords_trigger();
       public          postgres    false            �            1255    43845     audit_passwords_update_trigger()    FUNCTION       CREATE FUNCTION public.audit_passwords_update_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO audit_passwords (date_time, record_id, what_done)
    VALUES (CURRENT_TIMESTAMP, NEW.password_id, 'UPDATE');
    RETURN NEW;
END;
$$;
 7   DROP FUNCTION public.audit_passwords_update_trigger();
       public          postgres    false            �            1259    43810    audit_keylogs    TABLE     �   CREATE TABLE public.audit_keylogs (
    audit_id integer NOT NULL,
    date_time timestamp without time zone NOT NULL,
    record_id integer NOT NULL,
    what_done text NOT NULL
);
 !   DROP TABLE public.audit_keylogs;
       public         heap    postgres    false            �            1259    43809    audit_keylogs_audit_id_seq    SEQUENCE     �   CREATE SEQUENCE public.audit_keylogs_audit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.audit_keylogs_audit_id_seq;
       public          postgres    false    219            ,           0    0    audit_keylogs_audit_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.audit_keylogs_audit_id_seq OWNED BY public.audit_keylogs.audit_id;
          public          postgres    false    218            �            1259    43819    audit_passwords    TABLE     �   CREATE TABLE public.audit_passwords (
    audit_id integer NOT NULL,
    date_time timestamp without time zone NOT NULL,
    record_id integer NOT NULL,
    what_done text NOT NULL
);
 #   DROP TABLE public.audit_passwords;
       public         heap    postgres    false            �            1259    43818    audit_passwords_audit_id_seq    SEQUENCE     �   CREATE SEQUENCE public.audit_passwords_audit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.audit_passwords_audit_id_seq;
       public          postgres    false    221            -           0    0    audit_passwords_audit_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.audit_passwords_audit_id_seq OWNED BY public.audit_passwords.audit_id;
          public          postgres    false    220            �            1259    43788    table_for_keylogs    TABLE     �   CREATE TABLE public.table_for_keylogs (
    keylog_id integer NOT NULL,
    mail_id text NOT NULL,
    date_time timestamp without time zone NOT NULL,
    keylog_hash text NOT NULL
);
 %   DROP TABLE public.table_for_keylogs;
       public         heap    postgres    false            �            1259    43787    table_for_keylogs_keylog_id_seq    SEQUENCE     �   CREATE SEQUENCE public.table_for_keylogs_keylog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.table_for_keylogs_keylog_id_seq;
       public          postgres    false    215            .           0    0    table_for_keylogs_keylog_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.table_for_keylogs_keylog_id_seq OWNED BY public.table_for_keylogs.keylog_id;
          public          postgres    false    214            �            1259    43799    table_for_passwords    TABLE     �   CREATE TABLE public.table_for_passwords (
    password_id integer NOT NULL,
    mail_id text NOT NULL,
    date_time timestamp without time zone NOT NULL,
    password_hash text NOT NULL
);
 '   DROP TABLE public.table_for_passwords;
       public         heap    postgres    false            �            1259    43798 #   table_for_passwords_password_id_seq    SEQUENCE     �   CREATE SEQUENCE public.table_for_passwords_password_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 :   DROP SEQUENCE public.table_for_passwords_password_id_seq;
       public          postgres    false    217            /           0    0 #   table_for_passwords_password_id_seq    SEQUENCE OWNED BY     k   ALTER SEQUENCE public.table_for_passwords_password_id_seq OWNED BY public.table_for_passwords.password_id;
          public          postgres    false    216            |           2604    43813    audit_keylogs audit_id    DEFAULT     �   ALTER TABLE ONLY public.audit_keylogs ALTER COLUMN audit_id SET DEFAULT nextval('public.audit_keylogs_audit_id_seq'::regclass);
 E   ALTER TABLE public.audit_keylogs ALTER COLUMN audit_id DROP DEFAULT;
       public          postgres    false    219    218    219            }           2604    43822    audit_passwords audit_id    DEFAULT     �   ALTER TABLE ONLY public.audit_passwords ALTER COLUMN audit_id SET DEFAULT nextval('public.audit_passwords_audit_id_seq'::regclass);
 G   ALTER TABLE public.audit_passwords ALTER COLUMN audit_id DROP DEFAULT;
       public          postgres    false    221    220    221            z           2604    43791    table_for_keylogs keylog_id    DEFAULT     �   ALTER TABLE ONLY public.table_for_keylogs ALTER COLUMN keylog_id SET DEFAULT nextval('public.table_for_keylogs_keylog_id_seq'::regclass);
 J   ALTER TABLE public.table_for_keylogs ALTER COLUMN keylog_id DROP DEFAULT;
       public          postgres    false    215    214    215            {           2604    43802    table_for_passwords password_id    DEFAULT     �   ALTER TABLE ONLY public.table_for_passwords ALTER COLUMN password_id SET DEFAULT nextval('public.table_for_passwords_password_id_seq'::regclass);
 N   ALTER TABLE public.table_for_passwords ALTER COLUMN password_id DROP DEFAULT;
       public          postgres    false    216    217    217            #          0    43810    audit_keylogs 
   TABLE DATA           R   COPY public.audit_keylogs (audit_id, date_time, record_id, what_done) FROM stdin;
    public          postgres    false    219   �<       %          0    43819    audit_passwords 
   TABLE DATA           T   COPY public.audit_passwords (audit_id, date_time, record_id, what_done) FROM stdin;
    public          postgres    false    221   �A                 0    43788    table_for_keylogs 
   TABLE DATA           W   COPY public.table_for_keylogs (keylog_id, mail_id, date_time, keylog_hash) FROM stdin;
    public          postgres    false    215   �H       !          0    43799    table_for_passwords 
   TABLE DATA           ]   COPY public.table_for_passwords (password_id, mail_id, date_time, password_hash) FROM stdin;
    public          postgres    false    217   �I       0           0    0    audit_keylogs_audit_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.audit_keylogs_audit_id_seq', 128, true);
          public          postgres    false    218            1           0    0    audit_passwords_audit_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.audit_passwords_audit_id_seq', 186, true);
          public          postgres    false    220            2           0    0    table_for_keylogs_keylog_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.table_for_keylogs_keylog_id_seq', 201, true);
          public          postgres    false    214            3           0    0 #   table_for_passwords_password_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.table_for_passwords_password_id_seq', 607, true);
          public          postgres    false    216            �           2606    43817    audit_keylogs audit_keylogs_pk 
   CONSTRAINT     b   ALTER TABLE ONLY public.audit_keylogs
    ADD CONSTRAINT audit_keylogs_pk PRIMARY KEY (audit_id);
 H   ALTER TABLE ONLY public.audit_keylogs DROP CONSTRAINT audit_keylogs_pk;
       public            postgres    false    219            �           2606    43826 "   audit_passwords audit_passwords_pk 
   CONSTRAINT     f   ALTER TABLE ONLY public.audit_passwords
    ADD CONSTRAINT audit_passwords_pk PRIMARY KEY (audit_id);
 L   ALTER TABLE ONLY public.audit_passwords DROP CONSTRAINT audit_passwords_pk;
       public            postgres    false    221                       2606    43797 /   table_for_keylogs table_for_keylogs_mail_id_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.table_for_keylogs
    ADD CONSTRAINT table_for_keylogs_mail_id_key UNIQUE (mail_id);
 Y   ALTER TABLE ONLY public.table_for_keylogs DROP CONSTRAINT table_for_keylogs_mail_id_key;
       public            postgres    false    215            �           2606    43795 &   table_for_keylogs table_for_keylogs_pk 
   CONSTRAINT     k   ALTER TABLE ONLY public.table_for_keylogs
    ADD CONSTRAINT table_for_keylogs_pk PRIMARY KEY (keylog_id);
 P   ALTER TABLE ONLY public.table_for_keylogs DROP CONSTRAINT table_for_keylogs_pk;
       public            postgres    false    215            �           2606    43808 3   table_for_passwords table_for_passwords_mail_id_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.table_for_passwords
    ADD CONSTRAINT table_for_passwords_mail_id_key UNIQUE (mail_id);
 ]   ALTER TABLE ONLY public.table_for_passwords DROP CONSTRAINT table_for_passwords_mail_id_key;
       public            postgres    false    217            �           2606    43806 *   table_for_passwords table_for_passwords_pk 
   CONSTRAINT     q   ALTER TABLE ONLY public.table_for_passwords
    ADD CONSTRAINT table_for_passwords_pk PRIMARY KEY (password_id);
 T   ALTER TABLE ONLY public.table_for_passwords DROP CONSTRAINT table_for_passwords_pk;
       public            postgres    false    217            �           2620    43843 (   table_for_keylogs keylogs_delete_trigger    TRIGGER     �   CREATE TRIGGER keylogs_delete_trigger AFTER DELETE ON public.table_for_keylogs FOR EACH ROW EXECUTE FUNCTION public.audit_keylogs_delete_trigger();
 A   DROP TRIGGER keylogs_delete_trigger ON public.table_for_keylogs;
       public          postgres    false    224    215            �           2620    43841 (   table_for_keylogs keylogs_insert_trigger    TRIGGER     �   CREATE TRIGGER keylogs_insert_trigger AFTER INSERT ON public.table_for_keylogs FOR EACH ROW EXECUTE FUNCTION public.audit_keylogs_trigger();
 A   DROP TRIGGER keylogs_insert_trigger ON public.table_for_keylogs;
       public          postgres    false    215    222            �           2620    43842 (   table_for_keylogs keylogs_update_trigger    TRIGGER     �   CREATE TRIGGER keylogs_update_trigger AFTER UPDATE ON public.table_for_keylogs FOR EACH ROW EXECUTE FUNCTION public.audit_keylogs_update_trigger();
 A   DROP TRIGGER keylogs_update_trigger ON public.table_for_keylogs;
       public          postgres    false    215    223            �           2620    43849 ,   table_for_passwords passwords_delete_trigger    TRIGGER     �   CREATE TRIGGER passwords_delete_trigger AFTER DELETE ON public.table_for_passwords FOR EACH ROW EXECUTE FUNCTION public.audit_passwords_delete_trigger();
 E   DROP TRIGGER passwords_delete_trigger ON public.table_for_passwords;
       public          postgres    false    217    227            �           2620    43847 ,   table_for_passwords passwords_insert_trigger    TRIGGER     �   CREATE TRIGGER passwords_insert_trigger AFTER INSERT ON public.table_for_passwords FOR EACH ROW EXECUTE FUNCTION public.audit_passwords_trigger();
 E   DROP TRIGGER passwords_insert_trigger ON public.table_for_passwords;
       public          postgres    false    217    225            �           2620    43848 ,   table_for_passwords passwords_update_trigger    TRIGGER     �   CREATE TRIGGER passwords_update_trigger AFTER UPDATE ON public.table_for_passwords FOR EACH ROW EXECUTE FUNCTION public.audit_passwords_update_trigger();
 E   DROP TRIGGER passwords_update_trigger ON public.table_for_passwords;
       public          postgres    false    217    226            #   �  x�}�K��6E��U��!�I�Ӄ A$f���U%����@O������w��B_��Ccg'��d���o?����߿ə�c�N��������������C��J�|���/��� �)+E7��$�1�7�F�)& ��yCf�F����Kj#��(� �=$l�3j��Q�	���z��49d��~FY|~Vu��(f#��t���)�n�nTqT!���n\qq���Ɩ�R�J��7�qa����C�w[|cKbV w[|cKI矺-�����m�-��ؤ��[jgZ�-����z٤��[��tU|�JKQ�Uɍ*�����UNX���U��IW%7���&]�ܨ
SO��FU�dǦ]�ܨ��o����TT@�vS�L����a�����v��#ioR�#鍤G2ɏd6R�j�>�(�7i�$5�Ind<����GG��#i��ё4G��H�#{t$͑=:���isd���9�GG���Q#������ɋ����_-dK�/��%�Gْ����l���Q'�%�Gْ����l����B���#:�o�TDC��W��	�<(z�=�z"��O`��R�3��lq�<�-��G��v"e �=���?s�8�3�1��DG����"�d��"��-���#šc'���g����f{�E{G��%f��:����sѤ3i�>4�t����g���bn�l���'�Sӡ�o�m���g4�1���	2��L�@b��JpiV��O(�����`T+��3(���[��3��N\
C�Dߋ�cc��٭ގո�T�&�-R�4]AN\��e��h5M�5q��桘�{Q���I��p�*��&;�V�D߫ڙ�W
z��\G���O,�	J*K^s�h7T��Σк�X���JEQ� �z��e���/�(UZ�c��������uiЕ�5힉�huh��P/6M̅�Ŷu��,f[N�nXO0�~�`���C�lخ� 4�,?��e�~�����sǽO�/����>��N�F�aܱ����UE�����s���0/S�.C2�+l8������Y���c��H�_5w4�/8y�/�-�g����la����36D�$�;����f���	���K�T��Sz_�%6W�c7�����Ԙ�����`t�s������|�b��p��	/?ܰ^a��Q�w�mve�N5fMx?�g�f����ŚZ|��x�8��<�^��-��?��o���I0�      %   �  x�}�Kn�6���*���K�<+p3�@q[�1���Q��q~ڒ���:�>J"eݸ���	�;�i����o?�����^�kO��q������ԝJ��7��篿��z�mN���)�}Ev�H*gT�o�.Bu������_��o�ފ�=����ƏW��hod��#*��&5Du�6� :�6Ek)��
����W��A��JW�$M��h�����i���&iZ}�v�സ,Pil�ⴘ��J���5~=�PY���6�Te]���X1W٦(b�Q1Yynk��Ȧh�綸���)��-.N+��xn�cgŐ��dn��=��Ж�m1E��Ж�m1Sk�ڒ�-��OC[2�Ţ����d!K«n��d!KK$�f(K���|3�%Y�F (K��Id��,]ȪE����t!���@Q�.dU/��e�BV\��e�B��Ȗ��ta+��um��V�YE�hK����rX?��Ef˰�}�i�%��~K�ui�UO�nI�oIRnIRoI�nI�ޒȉ#n{e�R���8����N=IGu�HpT'��Gu�HpT'��Gu�HpT'��Gu�Hl�}{yOr�H,:'��Ĳs��I*8�# ��O	�|�Hp�G@�#�8�����'��v#ָ������'��Gm��I28jGOR`F-;�#�c��M�:�����C�l/�LV8R�
^6��,�6-���I��������95�G!Z�Gq��mG���Qq�c�U��X�h}�ӂ�5v41.BOҸ�qti]�Ҿ��r�2�W�{֫�=
���5�[�F���Mk�S�CR�z[��Ŝ)5`�/Xo#�Ԁ��92� �-Z۸F��S�B�lE��YGV�ن��Y;��()�J����)�␡y%��h�bS����/�(#�S�C%����a���0�3̯߳�T�َ,ݲX�񙭇j�9V�"��dkӑĩ)"�9l\�sOj��l7#'�TO0q)���8	�"�g1�����b���݉E�|vGM��q�6#O	�gy���<�aJ����9'�l�n����+�g{k�����0��,o�m�N�E�m�"OFr67��u����,#{��ؖƽ��ǫa�ڸ�[Z	������]즖v�\�=�H�1���_���q�YV�~�,y:�m��E!�_A]{-|D�$��9��t�a�m��9�X-{\�}���:樒b��+&>u��ɱj	a�czE�c�O�ǎ��&�vLbhx��s�7�{�����\��M�Buk���'�jx�PɻN뙵Cy�y9B���=�V�b.�sM/�2�;�.�l��ܼ<&�.��{�2�I��aw���b���E�'�\����W�h<0�#f���]f1���.���.�2�����q�Fӣ�N�]�}��%�4��`�{�ps�y�W/�>�^m���Ջ���*�[�:�xί^�e}ԋ�>>������#N����M4��.1��4p��qn���cv���U٭ĩi�r�ѵ-�V�VNW�g8*�Q����6F~F���R�����c``�ʲ��̌@S�H�s8�no&)�\ΰ�>����@9�<�9�F纩�cӳ��q��Gɪ�/au��pJN��G��󶂻8O�O�(+j�y���Q+8��Ҩ������b�x�H��]��,`�Cw�2FMO0�q�j�ѡX�z���\�8�|6�{0�������?ɴJW           x��нNA��z�*��ٜsfΙٍ1"��P�����H� �6^�C��4�_��{�qsu�����UL�(+�w��z3����k����:�7���'c��NCw�2
P���4�`=8Fd��%C�=a���n��b�2������ ��C���T��h�K}HH.!�Ā-Z}������碈.�F�eBp56��$��\b.R2"����U�c���^��(p�*聤��l4�[m�_2��瘝i߻�m D〉      !   {  x����n�@�k����ٙ�]۪�rHi�UmӦ�����Di��w�^D]��YB�矃&�7'r=��+�F
��-n����b����.��z���f�dӻ�����mݟ���+9NU���ڼ`���h�)]�V��E!�F������V�����F���01�R����Qq�*1�$�d	E��������㇑�A���HB� �LѤ��"�dF����Jֽ�$�8.���H���wS�W�3}��L%נu�L~�#m�0NY��T�����Ɓ�%7G��b��2�ϊ<ј��a�S�`$�ER����C����M�{5r�RQwR�npZ�)�}�z7h¢l��P�8��8��JH9$R
�R�6*:�q���j̲S���I��]l���羏㇙�����A�65Ƶ��/��ӽ�2\#5��#3�d�j��62.�sB]�Y��ŧ������L�yP�M"��fVԢ񩞍�M5RS�Nl3�J�bߧz��@�E���SU�$�}�W�#_�5��R�ڤJ�8�5N�R ��F'r�TU-��_c{>p��#5�㩲��8���}0�z�ۋ|��ʦ������J�]P�7ǋ-. �����^��y�����EQ�J̒�     