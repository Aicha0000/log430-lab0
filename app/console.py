"""
Application console pour la gestion d’un système de caisse : produits, ventes, retours et stock.
"""

from app.models import Produit, Vente, LigneVente
from app.persistance.db import session

def afficher_console_menu():
    print("Bienvenue dans le Menu Caisse")
    print("1. Ajouter un produit")
    print("2. Afficher les produits")
    print("3. Enregistrer une vente")
    print("4. Gérer les retours")
    print("5. Rechercher un produit")
    print("6. Quitter")


def afficher_statut_stock(produit):
    if produit.stock == 0:
        print(f"Produit '{produit.nom}' est en rupture.")
    elif produit.stock < 2:
        print(f"Produit '{produit.nom}' a un stock très faible.")
    else:
        print(f"Produit '{produit.nom}' est en stock.")


def verifier_coherence_stock(verbose=True):
    erreurs = False
    produits_negatifs = session.query(Produit).filter(Produit.stock < 0).all()
    if produits_negatifs:
        erreurs = True
        print("ATTENTION: Stock négatif pour :")
        for p in produits_negatifs:
            print(f"  - {p.nom} (Stock: {p.stock})")
    if not erreurs and verbose:
        print("Aucun problème détecté.")
    return not erreurs


def ajouter_produit():
    try:
        nom = input("Nom du produit: ")
        prix = float(input("Prix: "))
        description = input("Description: ")
        stock = int(input("Stock: "))
        if prix < 0 or stock < 0:
            print("Prix ou stock invalide.")
            return
        produit = Produit(nom=nom, prix=prix, description=description, stock=stock)
        session.add(produit)
        session.commit()
        print(f"Produit '{nom}' ajouté.")
    except ValueError:
        print("Entrée invalide.")


def afficher_produits():
    produits = session.query(Produit).all()
    if not produits:
        print("Aucun produit disponible.")
        return
    print("\nListe des produits:")
    for p in produits:
        print(f"ID: {p.id}, Nom: {p.nom}, Prix: {p.prix}, Desc: {p.description}, Stock: {p.stock}")
        afficher_statut_stock(p)
    verifier_coherence_stock(verbose=False)


def rechercher_produit():
    print("\nRecherche de produit:")
    print("1. Par ID\n2. Par nom")
    choix = input("Choix: ")
    if choix == '1':
        try:
            pid = int(input("ID produit: "))
            p = session.query(Produit).filter(Produit.id == pid).first()
            if p:
                print(f"Trouvé: {p.nom} - {p.stock} en stock")
            else:
                print("Produit introuvable.")
        except ValueError:
            print("ID invalide.")
    elif choix == '2':
        nom = input("Nom produit: ")
        ps = session.query(Produit).filter(Produit.nom.contains(nom)).all()
        for p in ps:
            print(f"ID: {p.id}, Nom: {p.nom}, Stock: {p.stock}")
            afficher_statut_stock(p)


def enregistrer_vente():
    print("\nEnregistrement de vente")
    if not verifier_coherence_stock():
        if input("Continuer malgré incohérences? (oui/non): ").lower() != 'oui':
            return
    transaction = session.begin()
    try:
        vente = Vente(total=0.0)
        session.add(vente)
        session.flush()
        total = 0.0
        while True:
            pid = input("ID produit (ou 'fin'): ")
            if pid.lower() == 'fin':
                break
            try:
                produit = session.query(Produit).filter(Produit.id == int(pid)).with_for_update().first()
                if not produit or produit.stock == 0:
                    print("Produit invalide ou en rupture.")
                    continue
                qty = int(input(f"Quantité pour {produit.nom}: "))
                if qty <= 0 or qty > produit.stock:
                    print("Quantité invalide ou stock insuffisant.")
                    continue
                produit.stock -= qty
                session.add(LigneVente(vente_id=vente.id, produit_id=produit.id, quantite=qty, prix_unitaire=produit.prix))
                total += qty * produit.prix
            except ValueError:
                print("Entrée invalide.")
        if total > 0:
            vente.total = total
            transaction.commit()
            print(f"Vente enregistrée. Total: {total} $")
        else:
            transaction.rollback()
            print("Vente annulée.")
    except Exception as e:
        transaction.rollback()
        print(f"Erreur: {e}")


def gerer_retours():
    print("\nRetour et Annulation de vente")
    ventes = session.query(Vente).filter(Vente.statut == 'active').all()
    if not ventes:
        print("Aucune vente active.")
        return
    for v in ventes:
        print(f"Vente {v.id} - Total: {v.total} $")
    try:
        vid = int(input("ID vente à annuler: "))
        vente = session.query(Vente).filter(Vente.id == vid, Vente.statut == 'active').with_for_update().first()
        if not vente:
            print("Vente invalide ou déjà annulée.")
            return
        if input("Confirmer annulation ? (oui/non): ").lower() != 'oui':
            return
        for l in vente.lignes:
            p = session.query(Produit).filter(Produit.id == l.produit_id).with_for_update().first()
            p.stock += l.quantite
        vente.statut = 'annulee'
        session.commit()
        print(f"Vente {vente.id} annulée.")
    except ValueError:
        print("Entrée invalide.")
    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")


def main():
    print("\nVérification initiale du stock...")
    verifier_coherence_stock()
    while True:
        afficher_console_menu()
        choix = input("Choix: ")
        if choix == '1':
            ajouter_produit()
        elif choix == '2':
            afficher_produits()
        elif choix == '3':
            enregistrer_vente()
        elif choix == '4':
            gerer_retours()
        elif choix == '5':
            rechercher_produit()
        elif choix == '6':
            print("Bye !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()

