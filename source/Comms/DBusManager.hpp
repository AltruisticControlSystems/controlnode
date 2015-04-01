//-----------------------------------------------------------------------------
// DBusManager.hpp
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
#ifndef COMMS_DBUS_MANAGER_HPP
#define COMMS_DBUS_MANAGER_HPP

#include <SingletonCxxQml.hpp>

#include <QObject>
#include <QtDBus/QDBusConnection>

// Forward Declarations
class ServerDBusClient;
class QString;

namespace Comms
{

class DBusManager: public cxxCore::SingletonCxxQml<DBusManager>
{
    Q_OBJECT

public:
    // SingletonCxxQml overrides
    virtual void init();
    virtual void deInit();

    // Local members
    void callOperation
        (
        unsigned int aNodeId,
        unsigned int aOperationId
        );

    bool getConnected() const;

public:
    // Signals
    Q_SIGNAL void callOperationReceived
        (
        unsigned int aNodeId,
        unsigned int aOperationId
        );

    Q_SIGNAL void connectionChanged();

private:
    DBusManager();

    bool registerConnection
        (
        const QString& aBusName,
        const QString& aPathName
        );
private:
    bool              mConnected;
    QDBusConnection   mDBusConnection;
    ServerDBusClient* mServerDBusClient;
}; // DBusManager
} // Comms

#endif // COMMS_DBUS_MANAGER_HPP
