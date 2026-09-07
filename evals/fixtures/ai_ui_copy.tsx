import { Banner, Button, EmptyState } from "../ui";

export const strings = {
  emptyTitle: "No Projects Yet",
  emptyBody:
    "Projects aren’t just folders — they’re the foundation of your workflow, bringing together tasks, files, and teammates in one vibrant workspace. Create your first project to unlock seamless collaboration.",
  emptyCta: "Get Started",
  syncError:
    "We encountered an issue while syncing your workspace. Our robust sync engine leverages a distributed queue, ensuring your changes are never lost. Please try again in a few moments.",
  upgradeHeading: "Why Upgrade to Pro?",
  upgradeBullets: [
    "**Unlimited projects**: Scale without limits.",
    "**Advanced permissions**: Fine-grained, flexible, and secure.",
    "**Priority support**: Our team is committed to your success.",
  ],
  quotaWarning:
    "You’ve used {used} of {limit} seats — a testament to how much your team has grown. Additionally, consider upgrading to accommodate future growth.",
};

export function ProjectsEmpty() {
  return (
    <EmptyState title={strings.emptyTitle} body={strings.emptyBody}>
      <Button>{strings.emptyCta}</Button>
    </EmptyState>
  );
}

export function SyncBanner() {
  return <Banner tone="error">{strings.syncError}</Banner>;
}
