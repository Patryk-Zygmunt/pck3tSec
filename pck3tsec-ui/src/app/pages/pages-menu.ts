import { NbMenuItem } from '@nebular/theme';

export const MENU_ITEMS: NbMenuItem[] = [
  {
    title: 'Dashboard',
    icon: 'home-outline',
    link: '/',
    home: true,
  },
  {
    title: 'Traffic',
    icon: 'globe-outline',
    link: '/traffic',
  },
  {
    title: 'Threats',
    icon: 'alert-triangle-outline',
    link: '/threats',
  },
  {
    title: 'Whitelist',
    icon: 'checkmark-square-2-outline',
    link: '/whitelist',
  },
  {
    title: 'Blacklist',
    icon: 'slash-outline',
    link: '/blacklist',
  },

];
