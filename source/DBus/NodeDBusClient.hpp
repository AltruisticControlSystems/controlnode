//-----------------------------------------------------------------------------
// NodeDBusClient.hpp
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

#include "com_altruistic_control_node.h"

#include <QtDBus/QDBusConnection>
#include <QString>

class NodeDBusClient: public ComAltruisticControlNodeInterface
{
    Q_OBJECT
public:
    NodeDBusClient
        (
        QString aBusName,                   //!< Name of the bus
        QString aObjectPath,                //!< DBus object path
        QDBusConnection const& aConnection, //!< DBus connection
        QObject* aParent                    //!< Optional parent object
        )
        : ComAltruisticControlNodeInterface
            (
            aBusName,
            aObjectPath,
            aConnection,
            aParent
            )
    {}

    virtual ~NodeDBusClient()
    {}
};

