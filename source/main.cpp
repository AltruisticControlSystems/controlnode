//-----------------------------------------------------------------------------
// Main.cpp
//
// Copyright Altruistic Control Systems and Kenneth Wells, 2015
// Author: Kenneth Wells
//-----------------------------------------------------------------------------
// This program is free software: you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
// FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
// more details.
//
// You should have received a copy of the GNU General Public License along
// with this program. If not, see <http://www.gnu.org/licenses/>.
//-----------------------------------------------------------------------------

#include <QtCore>
#include <QDebug>
#include <QtGui>
#include <QtQml/QtQml>
#include <QtQuick/QtQuick>

int main(int argc, char* argv[])
{
    //Q_INIT_RESOURCE(nodeUi);

    QGuiApplication nodeController(argc, argv);
    nodeController.setOrganizationName("Altruistic Control Systems");
    nodeController.setApplicationName("Controller Node");

    foreach(QScreen* screen, QGuiApplication::screens())
    {
        screen->setOrientationUpdateMask(
            Qt::LandscapeOrientation |
            Qt::PortraitOrientation |
            Qt::InvertedLandscapeOrientation |
            Qt::InvertedPortraitOrientation
            );
    }

    QQmlEngine engine;
    QQmlComponent mainWindow(&engine);
    QQuickWindow::setDefaultAlphaBuffer(true);
    mainWindow.loadUrl(QUrl("qrc:///main.qml"));

    if(mainWindow.isReady())
    {
        mainWindow.create();
    }
    else
    {
        qWarning() << mainWindow.errorString();
    }

    return nodeController.exec();
}
