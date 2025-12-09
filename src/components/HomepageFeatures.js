import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Physical AI Fundamentals',
    Svg: require('../../static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Comprehensive coverage of embodied intelligence principles and
        the distinction between traditional AI and Physical AI systems.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    Svg: require('../../static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        In-depth exploration of humanoid robot design, kinematics,
        dynamics, and control systems.
      </>
    ),
  },
  {
    title: 'Safety & Ethics',
    Svg: require('../../static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Critical focus on safety-first design principles and ethical
        considerations in humanoid robotics development.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}