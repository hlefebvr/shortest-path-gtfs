-- * 0 - Tramway, métro léger. Tout système de métro léger ou circulant au niveau de la rue au sein d'une zone métropolitaine.
-- * 1 - Métro. Tout système ferroviaire souterrain circulant au sein d'une zone métropolitaine.
-- * 2 - Train. Utilisé pour les trajets interurbains ou longue distance.
-- * 3 - Bus, car. Utilisé pour les lignes de bus courte et longue distance.
-- * 4 - Ferry. Utilisé pour le service de bateaux courte et longue distance.
-- * 5 - Tramway à traction par câble. Utilisé pour les tramways au niveau de la rue où le câble passe sous le véhicule.
-- * 6 - Téléphérique, télécabine. Généralement utilisé pour les moyens de transport aériens tractés par un câble, la cabine étant suspendue au câble.
-- * 7 - Funiculaire. Tout système ferroviaire conçu pour les pentes raides.

SELECT
    COUNT(*)
FROM
    routes
WHERE
    route_type = 1 -- Metro
    OR route_type = 3 -- Bus
    OR route_type = 2 -- Train