#include <QApplication>
#include <QtCore>

#include <stdlib.h>


int main(int argc, char* argv[])
{
    Q_INIT_RESOURCE(nodeUi);

    QApplication nodeController(argc, argv);
    app.setOrganizationName("Altruistic Control Systems");
    app.setApplicationName("Controller Node");

    AWindow mainWindow;

    AWindow.show();

    return app.exec();
}
