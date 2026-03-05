import {useState} from 'react';
import {Home} from './pages/Home/Home';
import {Page1} from './pages/Page1/Page1';
import {Page2} from './pages/Page2/Page2';
import {Navigation} from './components/Navigation/Navigation';
import {useNavigationService} from './services/useNavigationService';

import './styles/styles.scss';

export default () => {
  const {currentRoute, navigate} = useNavigationService();
  const [showDebug, setShowDebug] = useState(false);

  const renderContent = () => {
    switch (currentRoute) {
      case 'page1':
        return <Page1/>;
      case 'page2':
        return <Page2/>;
      case 'home':
      default:
        return <Home/>;
    }
  };

  return (
    <div className={'app-container'}>
      <Navigation
        currentRoute={currentRoute}
        onNavigate={navigate}
        showDebug={showDebug}
        onToggleDebug={() => setShowDebug(!showDebug)}
      />
      <div className='container'>

        {renderContent()}

        {showDebug && (
          <p id={"data-debug"}>
            lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
            dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
            ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat
            nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit
            anim id est laborum.
            <span>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ad consequatur, cum dignissimos eaque error excepturi exercitationem, incidunt maxime modi odit optio perspiciatis recusandae reprehenderit suscipit ullam ut voluptatem. Aliquid, omnis?</span><span>Architecto eius eum in provident quisquam? Ab amet aperiam asperiores atque beatae blanditiis, consequatur doloribus id illo impedit minima nam neque nisi, nobis pariatur possimus repudiandae similique sunt velit voluptatum?</span><span>Ab delectus doloribus exercitationem facere facilis fugit minus possimus quasi, quisquam quod? Amet beatae, earum excepturi molestias quod voluptatibus? Dignissimos, laborum libero. Laborum nam nesciunt temporibus? Accusamus blanditiis dignissimos id.</span><span>Alias, asperiores at atque distinctio dolores earum eos incidunt itaque magnam nemo odit possimus, quos rerum. Aliquam aspernatur consequatur, dolores earum eos eum ex itaque natus, provident quasi quidem, soluta?</span><span>Accusantium adipisci aliquid amet architecto assumenda consectetur dolor dolore dolorum eius excepturi facere fuga, laborum modi nemo nostrum optio perferendis perspiciatis porro possimus provident quod sit, tenetur vero voluptates voluptatibus.</span><span>Enim, eum eveniet fugit magni natus necessitatibus porro possimus, quae quaerat quos sunt tempore, voluptas! Ab consectetur cupiditate debitis eius eos facilis fuga ipsam laborum laudantium mollitia numquam, similique totam!</span><span>Exercitationem, neque, omnis. Animi aut cum, eaque et in molestiae neque non nulla officia provident quaerat quas quisquam rerum soluta velit veritatis, voluptatem. Consequuntur deserunt eum fugit, nemo reprehenderit tenetur.</span><span>Alias animi cupiditate doloremque ea facere impedit nesciunt pariatur perferendis praesentium quae quas qui quibusdam, repudiandae saepe similique sit, veniam. Alias aliquam dicta ducimus iusto nisi perferendis quam suscipit ut?</span><span>Ab blanditiis dignissimos earum nemo vel? Architecto blanditiis eum ipsa placeat quas. A, cupiditate deleniti laborum maiores omnis placeat quidem rem voluptatum! Animi, atque dolore eaque exercitationem non tempora veniam!</span><span>Alias aliquam aspernatur atque blanditiis commodi dolores dolorum error esse explicabo impedit in labore laborum minima nobis nostrum odit officiis optio quis recusandae reprehenderit sed sint tenetur, unde ut vitae.</span><span>A amet, atque commodi consectetur consequatur deleniti doloribus error et facere harum incidunt inventore iusto minus, modi nesciunt numquam omnis possimus qui quibusdam saepe sapiente soluta sunt ullam velit voluptate.</span><span>Dolorem error illum impedit libero maiores molestias nulla numquam quae reprehenderit vero. Aliquam consequuntur, corporis dolorum excepturi exercitationem in iste, labore maiores minus nam qui quis saepe voluptas voluptatem voluptatibus!</span><span>Fugiat impedit perspiciatis quam repellendus ut. Aliquid architecto aut dolorum eveniet molestiae mollitia placeat quidem repudiandae saepe voluptas. Et ipsa minus obcaecati qui veniam! Commodi ea porro praesentium quam tenetur.</span><span>Accusamus assumenda atque consequuntur distinctio, dolorem doloremque dolores est et eum explicabo facilis ipsum iure magni minus necessitatibus nobis nostrum perferendis placeat quasi quibusdam repellat tempore temporibus tenetur vitae voluptatem.</span><span>Alias fugiat ipsa iste laudantium minima nam natus quaerat similique. Animi aspernatur at consequatur dolorem dolores eaque ex fugit hic, maiores molestias natus nostrum numquam quis reiciendis soluta sunt veritatis.</span><span>Ab accusantium alias aperiam asperiores, aspernatur consectetur consequuntur dolor ea eligendi harum minus molestias nam natus nisi optio, quam quidem quos reprehenderit sit temporibus velit veritatis vitae voluptate voluptatem voluptates!</span><span>Accusantium adipisci aliquid commodi consectetur dolor dolores eligendi enim excepturi expedita explicabo fugiat, ipsam iusto necessitatibus numquam, omnis perspiciatis provident quisquam quos repellendus reprehenderit rerum voluptate voluptatem. Corporis, sapiente, voluptas!</span><span>Ab accusamus blanditiis commodi delectus, dolorem error facere facilis illum in iste magni minus molestias mollitia natus nostrum pariatur porro possimus praesentium quam reiciendis repellat repellendus repudiandae similique suscipit veritatis.</span><span>Consectetur, excepturi illo! Asperiores delectus deserunt, eligendi fuga ipsam labore maiores, minima modi nisi non praesentium reiciendis rem repellendus tenetur, ullam vitae voluptas. Aliquid, aperiam distinctio eveniet necessitatibus quaerat ullam!</span><span>Delectus inventore laboriosam laborum laudantium neque possimus reprehenderit totam ullam vel! Ad aut corporis cum debitis dolores eligendi enim est fugiat in incidunt maxime natus, quasi ratione saepe ut, voluptas.</span>
          </p>
        )}
      </div>
    </div>
  );
};
