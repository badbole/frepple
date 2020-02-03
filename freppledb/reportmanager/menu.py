# Copyright (C) 2019 by frePPLe bvba
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from freppledb.common.menus import MenuItem
from freppledb.menu import menu

from .views import ReportManager
from .models import SQLReport


def MyReports(request):
    result = []
    index = 1
    for x in (
        SQLReport.objects.all()
        .using(request.database)
        .filter(Q(user=request.user) | Q(public=True))
        .order_by("name")
    ):
        result.append(
            (
                index,
                x.name,
                MenuItem(
                    x.name,
                    url="/reportmanager/%s/" % x.id,
                    label=x.name,
                    index=index,
                    prefix=request.prefix,
                ),
            )
        )
        index += 1
    return result


menu.addGroup("custom", label=_("custom"), index=750)
menu.addItem("custom", "myreports", callback=MyReports, index=100)
menu.addItem("custom", "data", separator=True, index=1000)
menu.addItem(
    "custom", "reportmanager", url="/reportmanager/", report=ReportManager, index=1100
)