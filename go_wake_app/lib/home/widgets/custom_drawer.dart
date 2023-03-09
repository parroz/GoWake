import 'package:flutter/material.dart';

import '../../utils/app_routes.dart';
import 'custom_header.dart';

class CustomDrawer extends StatelessWidget {
  const CustomDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return NavigationDrawer(
      backgroundColor: Theme.of(context).colorScheme.onSecondary,
      surfaceTintColor: Theme.of(context).colorScheme.onSecondary,
      shadowColor: Theme.of(context).colorScheme.onSecondary,
      onDestinationSelected: (index) {
        if (index == 5) {
          Navigator.of(context).pop();
          Navigator.of(context).pushNamed(AppRoutes.SETTINGS);
        }
      },
      children: [
        MyHeaderDrawer(),
        const NavigationDrawerDestination(backgroundColor: Colors.white,
          icon: Icon(Icons.home),
          label: Text('Home/Events Calendar'),
        ),
        const NavigationDrawerDestination(
          icon: Icon(Icons.bar_chart),
          label: Text('Leaderboard'),
        ),
        const NavigationDrawerDestination(
          icon: Icon(Icons.edit),
          label: Text('Judge sheet'),
        ),
        const SizedBox(
          height: 40,
        ),
        const NavigationDrawerDestination(
          icon: Icon(Icons.logout),
          label: Text('Sign Out'),
        ),
        NavigationDrawerDestination(
          icon: const Icon(Icons.sync),
          label: Row(
            children: [
              const Text('Sync'),
              const SizedBox(width: 28),
              Text(
                '12/12/2012 às 12:12',
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ),
        ),
        const NavigationDrawerDestination(
          icon: Icon(Icons.settings),
          label: Text('Settings'),
        ),
      ],
    );
  }
}
