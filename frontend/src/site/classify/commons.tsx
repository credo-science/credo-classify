import { I18n } from "../../utils/i18n";

export interface CommonClassifyProps {
  user_id?: number;
  user_name?: string;

  team_id?: number;
  team_name?: string;
}

export function formatScopeInfo(_: I18n, props: CommonClassifyProps): string {
  const scopes: string[] = [];
  if (props.team_id) {
    scopes.push(`${_("classify.scope.team")}: ${props.team_name}`);
  }
  if (props.user_id) {
    scopes.push(`${_("classify.scope.user")}: ${props.user_name}`);
  }
  if (!props.user_id && !props.team_id) {
    scopes.push(_("classify.scope.all"));
  }

  return `${_("classify.scope")}: ${scopes.join(", ")}`;
}
