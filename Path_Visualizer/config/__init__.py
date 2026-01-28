"""
Modulo di configurazione globale dell'applicazione.

Espone l'istanza Singleton `settings` che contiene tutte le costanti
e i colori pre-caricati.
"""

from .manager import SettingsManager

# Istanziazione del Singleton
settings = SettingsManager()

"""
Istanza globale condivisa di :class:`SettingsManager`.

Usage:
    >>> from .config import settings
    >>> print(settings.WINDOW_TITLE)
    >>> brush = QBrush(settings.qcolors["wall"])
"""