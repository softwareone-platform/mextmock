import {Button} from '@swo/design-system/button';
import {Route} from '../../services/useNavigationService';

interface NavigationProps {
  currentRoute: Route;
  onNavigate: (route: Route) => void;
  showDebug: boolean;
  onToggleDebug: () => void;
}

/**
 * Navigation Component
 * Displays navigation buttons and debug controls
 */
export const Navigation = ({currentRoute, onNavigate, showDebug, onToggleDebug}: NavigationProps) => {
  return (
    <nav className='header'>
      <Button
        type='text'
        color='dark'
        onClick={() => onNavigate('home')}
        className={currentRoute === 'home' ? 'active' : ''}
      >
        Home
      </Button>
      <Button
        type='text'
        color='dark'
        onClick={() => onNavigate('page1')}
        className={currentRoute === 'page1' ? 'active' : ''}
      >
        Page 1
      </Button>
      <Button
        type='text'
        color='dark'
        onClick={() => onNavigate('page2')}
        className={currentRoute === 'page2' ? 'active' : ''}
      >
        Page 2
      </Button>
      <Button
        type='text'
        className="debug-toggle"
        onClick={onToggleDebug}
      >
        {showDebug ? 'Hide' : 'Show'} Debug
      </Button>
    </nav>
  );
};
