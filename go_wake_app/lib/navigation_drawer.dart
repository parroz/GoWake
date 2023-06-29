import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:go_wake_app/configuration/configuration_page.dart';
import 'package:go_wake_app/shared/constants.dart';
import 'package:go_wake_app/utils/app_routes.dart';
import 'package:go_wake_app/views/competitions/competitions_calendar_page.dart';

import 'package:provider/provider.dart';

import 'custom_header.dart';
import 'navigation_drawer_controller.dart';


class CustomNavigationDrawer extends StatefulWidget {
  const CustomNavigationDrawer({Key? key}) : super(key: key);

  @override
  State<CustomNavigationDrawer> createState() => _NavigationDrawerState();
}
class _NavigationDrawerState extends State<CustomNavigationDrawer> {
  @override
  void dispose() {
    super.dispose();
  }
  @override
  void initState() {
    super.initState();
    var controller = Provider.of<NavigationDrawerController>(context, listen: false);
    controller.addListener(() {
      if (controller.state == LoginState.SUCCESS) {
        Navigator.of(context).pushNamedAndRemoveUntil(
          AppRoutes.LOGIN,(Route<dynamic> route) => false,
        );
      }

    });
  }

  var currentPage = DrawerSections.home;
  @override
  Widget build(BuildContext context) {
    var container;
    if (currentPage == DrawerSections.home) {
      container = const CompetitionsCalendarPage();
    }else if (currentPage == DrawerSections.settings) {
      container = const ConfigurationPage();
    }

    return Scaffold(

      appBar: AppBar(centerTitle: true,
        title:  Image.asset(
          'lib/assets/logo_bar.png',
          height: 30,
        ),
        iconTheme: const IconThemeData(color: Colors.white),

        actions: const [

        ],
      ),
      body: container,
      drawer: Drawer(
        backgroundColor: Theme.of(context).colorScheme.background,
        child: SingleChildScrollView(
          child: Container(
            color: Theme.of(context).colorScheme.background,
            child: Column(
              children: [
                MyHeaderDrawer(),
                MyDrawerList(),
              ],
            ),
          ),
        ),
      ),
    );

  }
  Widget MyDrawerList() {
    return Container(
      color: Theme.of(context).colorScheme.background,
      padding: EdgeInsets.only(
        top: 15,
      ),
      child: Column(
        // shows the list of menu drawer
        children: [
          menuItem(1, "Home/Events Calendar", Icons.home,
              currentPage == DrawerSections.home ? true : false),
          // menuItem(2, "Leaderboard", Icons.bar_chart,
          //     currentPage == DrawerSections.leaderboard ? true : false),
          // menuItem(3, "Judge sheet", Icons.edit,
          //     currentPage == DrawerSections.judgeSheet ? true : false),
          const SizedBox(
            height: 40,
          ),
          const Divider(),
          menuItem(4, "Sign Out", Icons.logout,
              currentPage == DrawerSections.signOut ? true : false),
          menuItem(5, "Sync", Icons.sync,
             currentPage == DrawerSections.sync ? true : false),
          menuItem(6, "Settings", Icons.settings,
              currentPage == DrawerSections.settings ? true : false),
          Container(
            height: MediaQuery.of(context).size.height,color: Theme.of(context).colorScheme.background,
          )

        ],
      ),
    );
  }
  Widget menuItem(int id, String title, IconData icon, bool selected) {
    return Material(
      color: selected ? Theme.of(context).colorScheme.tertiary : Colors.transparent,
      child: Consumer<NavigationDrawerController>(
        builder: (BuildContext context, controller, widget) {
         return InkWell(
          onTap: () {
            Navigator.pop(context);
            setState(() {
              if (id == 1) {
                currentPage = DrawerSections.home;
              } else if (id == 2) {
                currentPage = DrawerSections.leaderboard;
              } else if (id == 3) {
                currentPage = DrawerSections.judgeSheet;
              } else if (id == 4) {
                currentPage = DrawerSections.signOut;
                controller.signOut();
              } else if (id == 5) {
              }else if (id == 6) {
                currentPage = DrawerSections.settings;
              }

            });
          },
          child: Padding(
            padding: EdgeInsets.all(15.0),
            child: Row(
              children: [
                Expanded(
                  child: Icon(
                    icon,
                    size: 20,
                    color: Theme.of(context).colorScheme.onSecondaryContainer,
                  ),
                ),
                Expanded(
                  flex: 3,
                  child: Text(
                    title,
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.onSecondaryContainer,
                      fontSize: 16,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
        }

      ),
    );
  }
}

enum DrawerSections {
  home,
  leaderboard,
  judgeSheet,
  signOut,
  sync,
  settings,
}