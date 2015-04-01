//-----------------------------------------------------------------------------
// DBusManager.cpp
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

#include "DBusManager.hpp"

#include "ServerDBusClient.hpp"

#include <QDebug>
#include <QString>

namespace Comms
{

//! init
//!
//! Method to init the manager
void DBusManager::init()
{
    mConnected = registerConnection(
        "com.altruistic.control.node",
        "/com/altruistic/control/node"
        );

    mServerDBusClient = new ServerDBusClient(
        "com.altruistic.control.server",
        "/com/altruistic/control/server",
        QDBusConnection::systemBus(),
        this
        );
}

//! deInit
//!
//! Method to deInit the manager
void DBusManager::deInit()
{
}

//! callOperation
//!
//! Method triggered via DBUS
void DBusManager::callOperation
    (
    unsigned int aNodeId,     //!< The ID of the node within the database who
                              //!< should do the operation
    unsigned int aOperationId //!< The ID of the operation that the node should
                              //!< perform
    )
{
    emit callOperationReceived(aNodeId,aOperationId);
}

//! getConnected
//!
//! Get the connectivity status
bool DBusManager::getConnected() const
{
    return mConnected;
}

//! registerConnection
//!
//! Register the DBus connections
bool DBusManager::registerConnection
    (
    const QString& aBusName,
    const QString& aPathName
    )
{
    bool result = false;

    QDBusReply<QDBusConnectionInterface::RegisterServiceReply> response =
        mDBusConnection.interface()->registerService
            (
            aBusName,
            QDBusConnectionInterface::ReplaceExistingService,
            QDBusConnectionInterface::AllowReplacement
            );

    if(!response.isValid() ||
        response.value() != QDBusConnectionInterface::ServiceRegistered)
    {
        qWarning() << aBusName.toLatin1() << response.error();
    }
    else
    {
        result = mDBusConnection.registerObject(aPathName, this);

        if(!result)
        {
            qWarning() << aPathName.toLatin1() << mDBusConnection.lastError().message();
        }
    }

    mConnected = result;

    emit connectionChanged();

    return result;
}

} // Comms
