# -*- coding: utf-8 -*-

# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""Kite installation widget."""

# Standard library imports
import sys

# Third-party imports
from qtpy.QtCore import QEvent, Qt, QUrl, Signal
from qtpy.QtGui import QDesktopServices, QMovie, QPixmap
from qtpy.QtWidgets import (QApplication, QDialog, QHBoxLayout, QMessageBox,
                            QLabel, QProgressBar, QPushButton, QVBoxLayout,
                            QWidget)

# Local imports
from spyder.config.base import _, get_image_path
from spyder.config.gui import is_dark_interface
from spyder.config.manager import CONF
from spyder.plugins.completion.kite.utils.install import (ERRORED, INSTALLING,
                                                          FINISHED)


class KiteIntegrationInfo(QWidget):
    """Initial Widget with info about the integration with Kite."""
    # Signal triggered for the 'Learn more' button
    sig_learn_more_button_clicked = Signal()
    # Signal triggered for the 'Install Kite' button
    sig_install_button_clicked = Signal()
    # Signal triggered for the 'Dismiss' button
    sig_dismiss_button_clicked = Signal()

    def __init__(self, parent):
        super(KiteIntegrationInfo, self).__init__(parent)
        # Images
        images_layout = QHBoxLayout()
        if is_dark_interface():
            icon_filename = 'spyder_kite.svg'
        else:
            icon_filename = 'spyder_kite_dark.svg'
        image_path = get_image_path(icon_filename)
        image = QPixmap(image_path)
        image_label = QLabel()
        image_label.setPixmap(image)

        images_layout.addStretch(0)
        images_layout.addWidget(image_label)
        images_layout.addStretch(0)

        # Label
        integration_label = QLabel(
            _('''Now Spyder can use <a href="https://kite.com/">Kite</a> to '''
              '''provide better and more accurate code completions in its '''
              '''editor <br>for the most important packages in the Python '''
              '''scientific ecosystem, such as Numpy, <br>Matplotlib and '''
              '''Pandas.<br><br>Would you like to install it or learn more '''
              '''about it?<br><br><i>Note:</i> Kite is free to use '''
              '''but is not an open source program.'''))
        integration_label.setOpenExternalLinks(True)

        # Buttons
        buttons_layout = QHBoxLayout()
        learn_more_button = QPushButton(_('Learn more'))
        learn_more_button.setAutoDefault(False)
        install_button = QPushButton(_('Install Kite'))
        install_button.setAutoDefault(False)
        dismiss_button = QPushButton(_('Dismiss'))
        dismiss_button.setAutoDefault(False)
        buttons_layout.addStretch(0)
        buttons_layout.addWidget(install_button)
        buttons_layout.addWidget(learn_more_button)
        buttons_layout.addWidget(dismiss_button)

        general_layout = QVBoxLayout()
        general_layout.addLayout(images_layout)
        general_layout.addWidget(integration_label)
        general_layout.addLayout(buttons_layout)
        self.setLayout(general_layout)

        learn_more_button.clicked.connect(self.sig_learn_more_button_clicked)
        install_button.clicked.connect(self.sig_install_button_clicked)
        dismiss_button.clicked.connect(self.sig_dismiss_button_clicked)


class KiteWelcome(QWidget):
    """Kite welcome info widget."""

    # Signal to check clicks on the installation button
    sig_install_button_clicked = Signal()
    # Signal to check clicks on the dismiss button
    sig_dismiss_button_clicked = Signal()

    def __init__(self, parent):
        super(KiteWelcome, self).__init__(parent)
        self.setFixedHeight(340)

        # Left side
        install_info = QLabel(
            _('''<big><b>Level up your completions with '''
              '''Kite</b></big><br><br>'''
              '''Kite is a native app that runs locally '''
              '''on your computer <br>and uses machine learning '''
              '''to provide advanced <br>completions.<br><br>'''
              '''&#10003; Specialized support for Python '''
              '''data analysis packages<br><br>'''
              '''&#10003; 1.5x more completions '''
              '''than the builtin engine<br><br>'''
              '''&#10003; Completions ranked by code context <br><br>'''
              '''&#10003; Full line code completions<br><br>'''
              '''&#10003; 100% local - no internet '''
              '''connection required<br><br>'''
              '''&#10003; 100% free to use<br><br>'''
              '''<a href="https://kite.com/spyder-integration">'''
              '''Learn more</a>'''))
        install_info.setOpenExternalLinks(True)

        # Right side
        action_layout = QVBoxLayout()
        install_gif_source = get_image_path('kite.gif')

        install_gif = QMovie(install_gif_source)
        install_gif.start()
        install_gif_label = QLabel()
        install_gif_label.setMovie(install_gif)

        button_layout = QHBoxLayout()
        install_button = QPushButton(_('Install Kite'))
        dismiss_button = QPushButton(_('Dismiss'))
        button_layout.addStretch(0)
        button_layout.addWidget(install_button)
        button_layout.addWidget(dismiss_button)
        button_layout.addStretch(0)

        action_layout.addWidget(install_gif_label)
        action_layout.addStretch(0)
        action_layout.addLayout(button_layout)

        # Layout
        general_layout = QHBoxLayout()
        general_layout.addWidget(install_info)
        general_layout.addLayout(action_layout)
        self.setLayout(general_layout)

        # Signals
        install_button.clicked.connect(self.sig_install_button_clicked)
        dismiss_button.clicked.connect(self.sig_dismiss_button_clicked)


class KiteInstallation(QWidget):
    """Kite progress installation widget."""

    # Signal to check clicks on the ok button
    sig_ok_button_clicked = Signal()
    # Signal to check clicks on the cancel button
    sig_cancel_button_clicked = Signal()

    def __init__(self, parent):
        super(KiteInstallation, self).__init__(parent)

        # Left side
        action_layout = QVBoxLayout()
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setFixedWidth(300)
        self._progress_label = QLabel(_('Downloading'))
        install_info = QLabel(
            _('''Kite comes with a native app called the Copilot <br>'''
              '''which provides you with real time <br>'''
              '''documentation as you code.<br><br>'''
              '''When Kite is done installing, the Copilot will <br>'''
              '''launch automatically and guide you throught the <br>'''
              '''rest of the setup process.'''))

        button_layout = QHBoxLayout()
        ok_button = QPushButton(_('OK'))
        cancel_button = QPushButton(_('Cancel'))
        button_layout.addStretch(0)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch(0)

        action_layout.addStretch(0)
        action_layout.addWidget(self._progress_label)
        action_layout.addWidget(self._progress_bar)
        action_layout.addWidget(install_info)
        action_layout.addStretch(0)
        action_layout.addLayout(button_layout)

        # Right side
        copilot_image_source = get_image_path('kite_copilot.png')

        copilot_image = QPixmap(copilot_image_source)
        copilot_label = QLabel()
        copilot_label.setPixmap(copilot_image)

        # Layout
        general_layout = QHBoxLayout()
        general_layout.addLayout(action_layout)
        general_layout.addWidget(copilot_label)

        self.setLayout(general_layout)

        # Signals
        ok_button.clicked.connect(self.sig_ok_button_clicked)
        cancel_button.clicked.connect(self.sig_cancel_button_clicked)

    def update_installation_status(self, status):
        """Update installation status (downloading, installing, finished)."""
        self._progress_label.setText(status)
        if status == INSTALLING:
            self._progress_bar.setRange(0, 0)

    def update_installation_progress(self, current_value, total):
        """Update installation progress bar."""
        self._progress_bar.setMaximum(total)
        self._progress_bar.setValue(current_value)


class KiteInstallerDialog(QDialog):
    """Kite installer."""
    def __init__(self, parent, kite_installation_thread):
        super(KiteInstallerDialog, self).__init__(parent)
        if sys.platform == 'darwin':
            self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint
                                | Qt.Tool)
        else:
            self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self._parent = parent
        self._installation_thread = kite_installation_thread
        self._integration_widget = KiteIntegrationInfo(self)
        self._welcome_widget = KiteWelcome(self)
        self._installation_widget = KiteInstallation(self)

        # Layout
        installer_layout = QVBoxLayout()
        installer_layout.addWidget(self._integration_widget)
        installer_layout.addWidget(self._welcome_widget)
        installer_layout.addWidget(self._installation_widget)
        self._welcome_widget.hide()
        self._installation_widget.hide()

        self.setLayout(installer_layout)

        # Signals
        self._installation_thread.sig_download_progress.connect(
            self._installation_widget.update_installation_progress)
        self._installation_thread.sig_installation_status.connect(
            self._installation_widget.update_installation_status)
        self._installation_thread.sig_installation_status.connect(
            self.finished_installation)
        self._installation_thread.sig_error_msg.connect(self._handle_error_msg)
        self._integration_widget.sig_learn_more_button_clicked.connect(
            self.welcome)
        self._integration_widget.sig_install_button_clicked.connect(
            self.install)
        self._integration_widget.sig_dismiss_button_clicked.connect(
            self.reject)
        self._welcome_widget.sig_install_button_clicked.connect(
            self.install)
        self._welcome_widget.sig_dismiss_button_clicked.connect(
            self.reject)
        self._installation_widget.sig_ok_button_clicked.connect(
            self.close_installer)
        self._installation_widget.sig_cancel_button_clicked.connect(
            self.reject)

    def _handle_error_msg(self, msg):
        """Handle error message with an error dialog."""
        error_message_dialog = QMessageBox(self._parent)
        error_message_dialog.setText(
            _('''<b>An error ocurred while Kite was installing!</b><br><br>'''
              '''You can follow our manual install instructions to<br>'''
              '''integrate Kite with Spyder yourself.'''))
        error_message_dialog.setWindowTitle(_('Kite install error'))

        get_help_button = QPushButton(_('Get Help'))
        get_help_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                    QUrl('https://kite.com/download')))
        error_message_dialog.addButton(get_help_button, QMessageBox.ActionRole)
        error_message_dialog.exec_()

    def center(self):
        """Center the dialog."""
        screen = QApplication.desktop().screenGeometry(0)
        x = screen.center().x() - self.width() / 2
        y = screen.center().y() - self.height() / 2
        self.move(x, y)

    def welcome(self):
        """Show welcome widget."""
        self._integration_widget.hide()
        self._installation_widget.hide()
        self._welcome_widget.setVisible(True)
        self.adjustSize()
        self.center()

    def install(self):
        """Initialize installation process and show install widget."""
        self._welcome_widget.hide()
        self._integration_widget.hide()
        self._installation_thread.install()
        self._installation_widget.setVisible(True)
        self.adjustSize()
        self.center()

    def cancel_install(self):
        """Cancel the installation in progress."""
        reply = QMessageBox.critical(
            self._parent, 'Spyder',
            _('Do you really want to cancel Kite installation?'),
            QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes and self._installation_thread.isRunning():
            self._installation_thread.cancelled = True
            self._installation_thread.quit()
            return True
        return False

    def finished_installation(self, status):
        """Handle finished installation."""
        if status == FINISHED:
            self.accept()

    def close_installer(self):
        """Close the installation dialog."""
        on_integration_widget = self._integration_widget.isVisible()
        if (self._installation_thread.status == ERRORED
                or self._installation_thread.status == FINISHED
                or on_integration_widget):
            self.accept()
        else:
            self.hide()

    def reject(self):
        """Qt method override."""
        on_welcome_widget = self._welcome_widget.isVisible()
        on_integration_widget = self._integration_widget.isVisible()
        on_installation_widget = self._installation_widget.isVisible()
        if on_installation_widget:
            if not self.cancel_install():
                return
        elif on_welcome_widget or on_integration_widget:
            CONF.set('kite', 'installation/enabled', False)
        super(KiteInstallerDialog, self).reject()


if __name__ == "__main__":
    from spyder.utils.qthelpers import qapplication
    app = qapplication()
    install_welcome = KiteWelcome(None)
    install_welcome.show()
    install_progress = KiteInstallation(None)
    install_progress.show()
    app.exec_()
