from odoo import http
import xmlrpc.client

def connexion_server():
    global url
    url = "http://localhost:8074"
    global db
    db = "formation"
    global username
    username = "baminatabella@gmail.com"
    global password
    password = "18163dc4bb303861994eb989f033acd6e21cd7a3"
    global common
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    # version = common.version()
    # print(version)
    global uid
    uid = common.authenticate(db, username, password, {})
    global models
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

class OdooController(http.Controller):
    @http.route('/page/', auth='public')
    def index(self, **kwargs):
        # print(uid)
        connexion_server()
        bar = models.execute_kw(db, uid, password,
                          'res.partner', 'check_access_rights',
                          ['read'], {'raise_exception': False})
        print(bar)
        var = models.execute_kw(db, uid, password,
            'res.partner', 'search',
            [[['is_company', '=', True]]])
        print(var)
        #pagination
        var2 = models.execute_kw(db, uid, password,
                          'res.partner', 'search',
                          [[['is_company', '=', True]]],
                          {'offset': 6, 'limit': 4})
        print(var2)
        # Count record
        nb = models.execute_kw(db, uid, password,
                          'res.partner', 'search_count',
                          [[['is_company', '=', True]]])
        print(nb)
        # Read records repere les champs
        ids = models.execute_kw(db, uid, password,
                                'res.partner', 'search',
                                [[['is_company', '=', True]]],
                                {'limit': 1})
        #correspondant a la ligne ids
        [record] = models.execute_kw(db, uid, password,
                                     'res.partner', 'read', [ids])
        # count the number of fields fetched by default
        print('bella ',len(record))

        #recupere seulement trois champs correspondant a ids
        champs = models.execute_kw(db, uid, password,
                          'res.partner', 'read',
                          [ids], {'fields': ['name', 'country_id', 'comment']})
        print(champs)

        # connaitre les informations sur les champs: nom des champs, leurs types, la description ...
        fields = models.execute_kw(
            db, uid, password, 'res.partner', 'fields_get',
            [], {'attributes': ['string', 'help', 'type']})
        print(fields)
        #Search and read
        cr = models.execute_kw(db, uid, password,
                          'res.partner', 'search_read',
                          [[['is_company', '=', True]]],
                          {'fields': ['name', 'country_id', 'comment'], 'limit': 5}) #si cette liste n'est pas fournie, elle récupérera tous les champs des enregistrements correspondants
        print(cr)
        #Create records
        id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
            'name': "New Partner",
        }])
        print(id)
        #Update records
        models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {
            'name': "Newer partner"
        }])
        # obtenir le nom de l'enregistrement après l'avoir modifié
        nom = models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])
        print(nom)

        #Delete records
        models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
        # check if the deleted record is still in the database
        trouve = models.execute_kw(db, uid, password,
                          'res.partner', 'search', [[['id', '=', id]]]) # une recherche
        print(trouve)

        # Inspection and introspection
        #un modèle personnalisé ne contiendra initialement que les champs intégrés disponibles sur tous les modèles:
        # models.execute_kw(db, uid, password, 'ir.model', 'create', [{
        #     'name': "Custom Model",
        #     'model': "x_custom_model",
        #     'state': 'manual',
        # }])
        # champs = models.execute_kw(
        #     db, uid, password, 'x_custom_model', 'fields_get',
        #     [], {'attributes': ['string', 'help', 'type']}) # liste vide, il va prendre tous les champs
        # print(champs)

        # ir.model.fields
        #Fournit des informations sur les champs des modèles Odoo et permet d'ajouter des champs personnalisés sans utiliser de code Python
        # id = models.execute_kw(db, uid, password, 'ir.model', 'create', [{
        #     'name': "Custom Model Bella",
        #     'model': "x_custom_bella",
        #     'state': 'manual',
        # }]) # cree un model
        # models.execute_kw(
        #     db, uid, password,
        #     'ir.model.fields', 'create', [{
        #         'model_id': id,
        #         'name': 'x_name',
        #         'ttype': 'char',
        #         'state': 'manual',
        #         'required': True,
        #     }]) # ajoute des champs suplementaires
        # record_id = models.execute_kw(
        #     db, uid, password,
        #     'x_custom_bella', 'create', [{
        #         'x_name': "test record",
        #     }]) # insere des valeurs
        # valeur = models.execute_kw(db, uid, password, 'x_custom_bella', 'read', [[record_id]]) # recupere le champs inserer
        # print(valeur)
        return "Bella"

    @http.route('/facture-liste/', auth='public')
    def list(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                 'account.move', 'search_read',
                                 [[]],
                                 {'fields': ['name', 'amount_total_signed','state', 'date'],'offset': 1, 'limit': 4}) # 4 premieres valeurs


        print(factures)
        output = "<h1> Liste de toutes les factures </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture['state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-liste-paye/', auth='public')
    def list_paye(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["payment_state", "=", 'paid' ]]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures payees </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-en-encours/', auth='public')
    def list_en_paiement(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["payment_state", "=", 'in_payment' ]]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures en paiement </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-partielle/', auth='public')
    def list_partielle_paiement(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["payment_state", "=", 'partial']]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures partiellement payees </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-liste-non-paye/', auth='public')
    def list_non_paye(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["payment_state", "=", 'not_paid' ]]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures non payees </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-extourne/', auth='public')
    def list_extourne_paiement(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["payment_state", "=", 'reversed']]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures extourné </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output


    @http.route('/facture-status-brouillon/', auth='public')
    def list_status_brouillon(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["state", "=", 'draft']]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures  brouillons </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-status-posted/', auth='public')
    def list_status_posted(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["state", "=", 'posted']]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures comptabilisées </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output

    @http.route('/facture-status-cancel/', auth='public')
    def list_status_cancel(self, **kwargs):
        connexion_server()
        factures = models.execute_kw(db, uid, password,
                                     'account.move', 'search_read',
                                     [[["state", "=", 'cancel']]],
                                     {'fields': ['name', 'amount_total_signed', 'state', 'date'], 'offset': 1,
                                      'limit': 4})  # 4 premieres valeurs

        print(factures)
        output = "<h1> Liste de toutes les factures Annulée </h1><br/>"
        output += "<ul>"
        for facture in factures:
            output += "<li>" + str(facture['date']) + ' --- ' + facture['name'] + ' --- ' + facture[
                'state'] + ' --- ' + str(facture['amount_total_signed']) + "</li>"
        output += "</ul>"
        return output