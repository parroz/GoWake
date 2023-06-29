import 'package:flutter/material.dart';

import 'package:provider/provider.dart';

import 'configuration_controller.dart';

class ConfigurationPage extends StatefulWidget {
  const ConfigurationPage({super.key});

  @override
  State<ConfigurationPage> createState() => _ConfigurationPageState();
}

class _ConfigurationPageState extends State<ConfigurationPage> {
  @override
  Widget build(BuildContext context) {

    var controller = Provider.of<ConfigurationController>(context, listen: false);
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.fromLTRB(20, 20, 20, 0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Settings',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 20),
            Text(
              'Theme',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 10),
            RadioListTile<ThemeMode>(
              value: ThemeMode.system,
              groupValue: controller.themeMode.value,
              title: const Text('System'),
              onChanged: controller.changeThemeMode,
            ),
            RadioListTile<ThemeMode>(
              value: ThemeMode.light,
              groupValue: controller.themeMode.value,
              title: const Text('Light'),
              onChanged: controller.changeThemeMode,
            ),
            RadioListTile<ThemeMode>(
              value: ThemeMode.dark,
              groupValue: controller.themeMode.value,
              title: const Text('Dark'),
              onChanged: controller.changeThemeMode,
            ),
            const SizedBox(height: 20),
            // Text(
            //   'Controlo de dados',
            //   style: Theme.of(context).textTheme.titleMedium,
            // ),
            const SizedBox(height: 10),
            // OutlinedButton(
            //   onPressed: () {},
            //   child: const Text('Apagar cache e reiniciar a app'),
            // )
          ],
        ),
      ),
    );
  }
}